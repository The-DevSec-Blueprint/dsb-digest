from os import environ
import requests
import json

API_TOKEN = "28f0bcdb8b767cf34e3ec3af784d65361644a43cbd2d2f0ccc83e42084fa97c54"
MEDIUM_API = "https://api.medium.com/v1"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
}


class MediumClient:

    def __init__(self) -> None:
        self.user_id = self._get_authenticated_user()["data"]["id"]

    def get_articles(self):
        response = requests.get(
            url=f"{MEDIUM_API}/users/{self.user_id}/publications",
            headers=DEFAULT_HEADERS,
        )

        return response.json()

    def publish_article(self, post_content):
        canonical_url = f"https://{post_content['frontmatterData']['domain']}/{post_content['frontmatterData']['slug']}"
        tags = post_content["frontmatterData"]["tags"].split(",")
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

        print(response.json())
        return response.json()

    def _get_authenticated_user(self):
        response = requests.get(
            url=f"{MEDIUM_API}/me",
            headers=DEFAULT_HEADERS,
        )

        return response.json()


if __name__ == "__main__":
    client = MediumClient()
    client.get_articles()
