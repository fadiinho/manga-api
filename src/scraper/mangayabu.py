import requests
from bs4 import BeautifulSoup
from typing import Any, List, Dict, cast
from urllib.parse import quote
from .base_scraper import BaseScraper

KEYS = ["id", "slug", "link", "title", "_links"]


# TODO: Better error handling
class MangaYabuScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://mangayabu.top")
        self._options = {"per_page": 1, "order": "asc"}

    def _build_url(self, path: str):
        url = f"{self.base_host}/{path}"
        for (key, value) in self._options.items():
            url += f"&{key}={value}"

        return url

    def set_options(self, options: Dict[str, Any]):
        for _, (k, v) in enumerate(options.items()):
            self._options[k] = v

        return self

    def parse_links(self, target: Dict[str, Any]) -> Dict[str, str] | str:
        result = {}
        try:
            target.pop("curies")
        except KeyError:
            pass

        for _, (key, value) in enumerate(target.items()):
            if type(value) is str and key == "href":
                return value

            if type(value) is list:
                for inner_value in value:
                    if key not in result:
                        result[key] = self.parse_links(inner_value)

        return result

    def parse_response(self, response: List[Dict[str, str]]):
        result: List[Dict[str, Any]] = []

        for item in response:
            _dict_result = {}
            for _, (k, v) in enumerate(item.items()):
                if k in KEYS:
                    _dict_result[k] = v

            result.append(_dict_result)

        for item in result:
            if item.get("_links"):
                item["_links"] = self.parse_links(item["_links"])

        return result

    def search(self, title: str):
        url = self._build_url(f"wp-json/wp/v2/posts?search={quote(title)}")

        response = self.client.get(url)

        return self.parse_response(response.json())

    def get_manga_by_id(self, manga_id: int):
        url = self._build_url(f"wp-json/wp/v2/posts/{manga_id}?")

        response = self.client.get(url)

        if not response.ok:
            print(url)
            raise RuntimeError("Manga not found!")

        return self.parse_response([response.json()])[0]

    def get_images_by_url(self, url):
        response = requests.get(url)

        html = response.content

        soup = BeautifulSoup(html, features="html.parser")

        images_div = soup.select("div.manga-content img")

        soup = BeautifulSoup(html, features="html.parser")

        if not images_div:
            raise RuntimeError("Images not found, manga url broken!")

        images: List[Dict[str, str]] = []
        for image in images_div:
            title = cast(str, image.get("title"))
            src = cast(str, image.get("src"))

            if not src or not title:
                continue

            images.append({ "pageTitle": title, "src": src})

        return images

    def get_images_by_id(self, manga_id: int):
        manga = self.get_manga_by_id(manga_id)

        url = manga["link"]

        images = self.get_images_by_url(url)

        return images
