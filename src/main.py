"""
This module is responsible for publishing posts to Medium and Dev.to.
"""

import re
import glob
import logging

import frontmatter

from client.devto_client import DevToClient  # pylint: disable=import-error
from client.medium_client import MediumClient  # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)


class PostPublisher:
    # pylint: disable=line-too-long
    """
    This class is responsible for publishing posts to Medium and Dev.to.
    """

    def __init__(self) -> None:
        self.devto_client = DevToClient()
        self.medium_client = MediumClient()
        self.non_updated_articles = []
        self.logging = logging.getLogger(__name__)

    def publish_to_devto(self):
        """
        Publishes and updates articles to Dev.TO.
        """
        md_files = self._get_list_of_markdown_files()

        for md_file in md_files:
            post_content = self._get_post_content(md_file)
            to_publish = not post_content["frontmatterData"]["saveAsDraft"]

            article_id, is_currently_published = self._find_published_article_devto(
                post_content
            )

            if article_id is None:
                self.logging.info(
                    "Publishing new article, %s",
                    post_content["frontmatterData"]["title"],
                )
                self.devto_client.publish_article(post_content, to_publish)
            else:
                markdown_content = self.devto_client.get_article(
                    article_id, is_currently_published
                )["body_markdown"]
                cleaned_markdown_content = self._remove_frontmatter(markdown_content)
                if (
                    cleaned_markdown_content != post_content["bodyMarkdown"]
                    or is_currently_published != to_publish
                ):
                    self.logging.info(
                        "Updating article, %s", post_content["frontmatterData"]["title"]
                    )
                    self.devto_client.update_article(
                        article_id, post_content, to_publish
                    )
                else:
                    self.logging.info(
                        "Article, %s, already published! No changes are needed.",
                        post_content["frontmatterData"]["title"],
                    )
                    self.non_updated_articles.append(md_file)

    def publish_to_medium(self):
        """
        Publishes and updates articles to Medium.
        """
        md_files = self._get_list_of_markdown_files()

        for md_file in md_files:
            if md_file in self.non_updated_articles:
                self.logging.info(
                    "Article, %s, already published! No changes are needed.",
                    md_file,
                )
                continue

            post_content = self._get_post_content(md_file)
            article_id, is_currently_published = self._find_published_article_devto(
                post_content
            )
            body_html = self.devto_client.get_article(
                article_id, is_currently_published
            )["body_html"]
            post_content["bodyHtml"] = body_html

            self.medium_client.publish_article(post_content)

    def _find_published_article_devto(self, post_content):
        """
        Finds and returns the ID of the published article.
        Args:
            post_content (dict): The post content.
        Returns:
            tuple: The ID of the published article and a boolean indicating whether the article is currently published.
        Raises:
            Exception: If there is an error finding the article.
        """
        all_articles = self.devto_client.get_articles()

        for article in all_articles:
            if article["type_of"] == "article":
                if article["title"] == post_content["frontmatterData"]["title"]:
                    self.logging.info(
                        "Found article, %s",
                        post_content["frontmatterData"]["title"],
                    )
                    article_id = article["id"]
                    is_currently_published = article["published"]

                    return article_id, is_currently_published

        return None, None

    def _get_post_content(self, md_file):
        """
        Gets the post content from the Markdown file.
        Args:
            md_file (str): The path to the Markdown file.
        Returns:
            dict: The post content.
        """
        with open(md_file, "r", encoding="utf-8") as f:
            markdown_text = f.read()
        frontmatter_data = frontmatter.loads(markdown_text)

        return {
            "frontmatterData": frontmatter_data,
            "bodyMarkdown": self._remove_frontmatter(markdown_text),
        }

    def _remove_frontmatter(self, markdown_text):
        """
        Removes the frontmatter from the Markdown text.
        Args:
            markdown_text (str): The Markdown text.
        Returns:
            str: The Markdown text without the frontmatter.
        """
        frontmatter_pattern = r"^---\n(.*?)\n---\n"
        markdown_text_without_frontmatter = re.sub(
            frontmatter_pattern, "", markdown_text, flags=re.DOTALL
        )
        return markdown_text_without_frontmatter

    def _get_list_of_markdown_files(self):
        """
        Returns a list of Markdown files in the current directory.
        Returns:
            list: A list of Markdown files.
        """
        # Use glob to find all Markdown files
        md_files = glob.glob("./*.md")

        # Exclude README.md from the list
        md_files = [file for file in md_files if not file.endswith("README.md")]
        return md_files


if __name__ == "__main__":
    publisher = PostPublisher()
    publisher.publish_to_devto()
    publisher.publish_to_medium()
