"""
This module contains the MediumClient class. It is responsible
for interacting with Medium APIs.
"""

from os import environ
import logging
import requests

logging.basicConfig(level=logging.INFO)

API_TOKEN = environ["MEDIUM_API_TOKEN"]
MEDIUM_API = "https://api.medium.com/v1"
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
}


class MediumClient:
    # pylint: disable=line-too-long,missing-timeout
    """
    Class for interacting with Medium APIs.
    """

    def __init__(self) -> None:
        self.logging = logging.getLogger(__name__)
        self.user_id = self._get_authenticated_user()["data"]["id"]

    def get_articles(self):
        """
        Gets published articles based on the user ID.
        Returns:
            list(dict): List of articles. Each article is a dictionary.
        Raises:
            Exception: If there is an error retrieving the articles.
        """
        response = requests.get(
            url=f"{MEDIUM_API}/users/{self.user_id}/publications",
            headers=DEFAULT_HEADERS,
        )

        self.logging.info("Retrieved articles: %s", response)
        return response.json()

    def publish_article(self, post_content):
        """
        Publishes an article based on the post content.
        Args:
            post_content (dict): The content of the post.
        Returns:
            dict: The response from the API.
        Raises:
            Exception: If there is an error publishing the article.
        """
        canonical_url = f"https://{post_content['frontmatterData']['domain']}/{post_content['frontmatterData']['slug']}"
        tags = post_content["frontmatterData"]["tags"].split(",")

        articles = self.get_articles()
        edit_postfix = " (edited)"
        for article in articles["data"]:
            article_name = article["name"]
            if article_name == post_content["frontmatterData"]["title"]:
                self.logging.info(
                    "Article already exists, setting name of the post...."
                )
                post_content["frontmatterData"]["title"] += edit_postfix
                break

        cover_image = post_content["frontmatterData"]["cover"]
        cover_image_html = f'<img src="{cover_image}" alt="Cover image" />'
        post_content["bodyHtml"] = cover_image_html + "\n\n" + post_content["bodyHtml"]

        data = {
            "title": post_content["frontmatterData"]["title"],
            "canonicalUrl": canonical_url,
            "contentFormat": "html",
            "content": post_content["bodyHtml"],
            "publishStatus": "unlisted",
            "notifyFollowers": True,
            "tags": tags,
        }

        response = requests.post(
            url=f"{MEDIUM_API}/users/{self.user_id}/posts",
            json=data,
            headers=DEFAULT_HEADERS,
        )

        if edit_postfix in post_content["frontmatterData"]["title"]:
            self.logging.info(
                "An existing article has been edited and has been published: %s",
                response,
            )
        else:
            self.logging.info(
                "New article has been published as 'unlisted'! %s", response
            )

        return response.json()

    def _get_authenticated_user(self):
        """
        Gets the authenticated user.
        Returns:
            dict: The response from the API.
        """
        response = requests.get(
            url=f"{MEDIUM_API}/me",
            headers=DEFAULT_HEADERS,
        )

        return response.json()
