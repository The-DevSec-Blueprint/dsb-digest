from os import environ
import requests
import logging

logging.basicConfig(level=logging.INFO)

API_TOKEN = environ.get("DEVTO_API_KEY")
ARTICLES_URL = "https://dev.to/api/articles"


class DevToClient:

    def __init__(self) -> None:
        self.logging = logging.getLogger(__name__)

    def publish_article(self, post_content, published):
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
            ARTICLES_URL, json=data, headers=self._generate_header()
        )

        if response.status_code == 201:
            self.logging.info("Blog post published successfully!")
            return response.json()
        else:
            raise Exception(f"Error publishing blog post: {response.text}")

    def update_article(self, article_id, post_content, published):
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

        response = requests.put(url, json=data, headers=self._generate_header())
        if response.status_code == 200:
            self.logging.info("Blog post updated successfully!")
            return response.json()
        else:
            raise Exception(f"Error updating blog post: {response.text}")

    def get_articles(self):
        url = f"{ARTICLES_URL}/me/all?per_page=1000"
        response = requests.get(url, headers=self._generate_header())
        if response.status_code == 200:
            self.logging.info("Articles have been retrieved properly: %s", response)
            return response.json()
        else:
            raise Exception(f"Error retrieving articles: {response.text}")

    def get_article(self, article_id, published):
        if published:
            response = requests.get(
                f"{ARTICLES_URL}/{article_id}", headers=self._generate_header()
            )
            return response.json()
        else:
            response = requests.get(
                f"{ARTICLES_URL}/me/unpublished?per_page=1000",
                headers=self._generate_header(),
            )
            list_of_articles = response.json()
            for article in list_of_articles:
                if article["id"] == article_id:
                    return article

    def _generate_header(self):
        print(API_TOKEN)
        headers = {
            "api_key": API_TOKEN,
            "Content-Type": "application/json",
            "accept": "application/vnd.forem.api-v1+json",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
        }
        return headers
