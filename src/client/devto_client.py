"""
This module is used to interact with the Dev.to API for
publishing articles and retrieving them.
"""

from os import environ
import logging
import requests

logging.basicConfig(level=logging.INFO)

API_TOKEN = environ.get("DEVTO_API_KEY")
ARTICLES_URL = "https://dev.to/api/articles"


class DevToClient:
    # pylint: disable=line-too-long,broad-exception-raised,missing-timeout
    """
    This class is used to interact with the Dev.to API for
    publishing articles and retrieving them.
    """

    def __init__(self) -> None:
        self.logging = logging.getLogger(__name__)

    def publish_article(self, post_content, published):
        """
        Function to publish an article to Dev.to.
        Args:
            post_content (dict): The content of the post.
            published (bool): Whether the post is published or not.
        Returns:
            dict: The response from the API.
        Raises:
            Exception: If there is an error publishing the post.
        """
        canonical_url = f"https://{post_content['frontmatterData']['domain']}/{post_content['frontmatterData']['slug']}"

        data = {
            "article": {
                "title": post_content["frontmatterData"]["title"],
                "canonical_url": canonical_url,
                "description": post_content["frontmatterData"]["subtitle"],
                "main_image": post_content["frontmatterData"]["cover"],
                "tags": post_content["frontmatterData"]["tags"],
                "body_markdown": post_content["bodyMarkdown"],
                "published": published,
            }
        }

        response = requests.post(
            ARTICLES_URL, json=data, headers=self._generate_authenticated_header()
        )

        if response.status_code == 201:
            self.logging.info("Blog post published successfully!")
            return response.json()

        raise Exception(f"Error publishing blog post: {response.text}")

    def update_article(self, article_id, post_content, published):
        """
        Function to update an existing article on Dev.to.
        Args:
            article_id (int): The ID of the article to update.
            post_content (dict): The content of the post.
            published (bool): Whether the post is published or not.
        Returns:
            dict: The response from the API.
        Raises:
            Exception: If there is an error updating the post.
        """
        url = f"{ARTICLES_URL}/{article_id}"

        canonical_url = f"https://{post_content['frontmatterData']['domain']}/{post_content['frontmatterData']['slug']}"
        data = {
            "article": {
                "title": post_content["frontmatterData"]["title"],
                "canonical_url": canonical_url,
                "description": post_content["frontmatterData"]["subtitle"],
                "main_image": post_content["frontmatterData"]["cover"],
                "tags": post_content["frontmatterData"]["tags"],
                "body_markdown": post_content["bodyMarkdown"],
                "published": published,
            }
        }

        response = requests.put(
            url, json=data, headers=self._generate_authenticated_header()
        )
        if response.status_code == 200:
            self.logging.info("Blog post updated successfully!")
            return response.json()

        raise Exception(f"Error updating blog post: {response.text}")

    def get_articles(self):
        """
        Function to get list of articles published by me.
        Returns:
            dict: The response from the API.
        Raises:
            Exception: If there is an error retrieving the articles.
        """
        url = f"{ARTICLES_URL}/me/all?per_page=1000"
        response = requests.get(url, headers=self._generate_authenticated_header())
        if response.status_code == 200:
            self.logging.info("Articles have been retrieved properly: %s", response)
            return response.json()

        raise Exception(f"Error retrieving articles: {response.text}")

    def get_article(self, article_id, published):
        """
        Function to get an article by ID.
        Args:
            article_id (int): The ID of the article to retrieve.
            published (bool): Whether the article is published or not.
        Returns:
            dict: The response from the API.
        """
        if published:
            response = requests.get(
                f"{ARTICLES_URL}/{article_id}",
                headers=self._generate_authenticated_header(),
            )
            return response.json()

        response = requests.get(
            f"{ARTICLES_URL}/me/unpublished?per_page=1000",
            headers=self._generate_authenticated_header(),
        )
        list_of_articles = response.json()
        for article in list_of_articles:
            if article["id"] == article_id:
                return article

        return None

    def _generate_authenticated_header(self):
        """
        Function to generate authenticated headers for the requests.
        Returns:
            dict: The authenticated header.
        """
        headers = {
            "api_key": API_TOKEN,
            "Content-Type": "application/json",
            "accept": "application/vnd.forem.api-v1+json",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
        }
        return headers
