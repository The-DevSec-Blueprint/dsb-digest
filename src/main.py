"""
This module is responsible for publishing posts to Dev.to.
"""

import re
import glob
import time
import logging
import frontmatter
from md_toc.api import build_toc

from client.devto_client import DevToClient  # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)


class PostPublisher:
    # pylint: disable=line-too-long, too-few-public-methods
    """
    This class is responsible for publishing posts to Dev.to.
    """

    def __init__(self) -> None:
        self.devto_client = DevToClient()
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

            time.sleep(5)  # Sleep for 5 seconds to avoid rate limiting

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

        # Remove frontmatter from markdown
        md_text_without_frontmatter = self._remove_frontmatter(markdown_text)

        # Adds TOC to the markdown text
        toc = build_toc(md_file)
        md_text_without_frontmatter = (
            "## Table of Contents\n" + toc + "\n" + md_text_without_frontmatter
        )

        # Removes center align for hashnode
        if 'align="center"' in md_text_without_frontmatter:
            self.logging.info("Removing center align for hashnode")
            md_text_without_frontmatter = md_text_without_frontmatter.replace(
                ' align="center"', ""
            )

        return {
            "frontmatterData": frontmatter_data,
            "bodyMarkdown": md_text_without_frontmatter,
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
