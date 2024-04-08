import re
import glob
import frontmatter
import logging

from client.devto_client import DevToClient

logging.basicConfig(level=logging.INFO)


class PostPublisher:
    def __init__(self) -> None:
        self.devto_client = DevToClient()
        self.logging = logging.getLogger(__name__)

    def publish_to_devto(self):
        all_articles = self.devto_client.get_articles()
        md_files = self._get_list_of_markdown_files()

        for md_file in md_files:
            post_content = self._get_post_content(md_file)
            to_publish = (
                True
                if post_content["frontmatterData"]["saveAsDraft"] is False
                else False
            )

            article_id = None
            is_currently_published = False
            for article in all_articles:
                # Check to see if article is in them
                if article["type_of"] == "article":
                    if article["title"] == post_content["frontmatterData"]["title"]:
                        self.logging.info(
                            "Found article, %s",
                            post_content["frontmatterData"]["title"],
                        )
                        article_id = article["id"]
                        is_currently_published = article["published"]
                        break

            if article_id is None:
                # Publish
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

    def _get_post_content(self, md_file):
        with open(md_file, "r") as f:
            markdown_text = f.read()
        frontmatter_data = frontmatter.loads(markdown_text)

        return {
            "frontmatterData": frontmatter_data,
            "bodyMarkdown": self._remove_frontmatter(markdown_text),
        }

    def _remove_frontmatter(self, markdown_text):
        frontmatter_pattern = r"^---\n(.*?)\n---\n"
        markdown_text_without_frontmatter = re.sub(
            frontmatter_pattern, "", markdown_text, flags=re.DOTALL
        )
        return markdown_text_without_frontmatter

    def _get_list_of_markdown_files(self):
        # Use glob to find all Markdown files
        md_files = glob.glob("./*.md")

        # Exclude README.md from the list
        md_files = [file for file in md_files if not file.endswith("README.md")]
        return md_files


if __name__ == "__main__":
    publisher = PostPublisher()
    publisher.publish_to_devto()
