from typing import Any, Dict
from ..scraper.mangayabu import MangaYabuScraper

mangayabu = MangaYabuScraper()


def search_by_name(search_term: str, search_options: Dict[str, Any] = {}):

    mangayabu.set_options(search_options)

    return mangayabu.search(search_term)


def get_manga_by_id(id: int):
    response = mangayabu.get_manga_by_id(id)

    return response


def get_images_by_id(id: int):
    response = mangayabu.get_images_by_id(id)

    return response
