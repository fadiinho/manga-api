from ..scraper.mangayabu import MangaYabuScraper

mangayabu = MangaYabuScraper()


def search_by_name(search_term: str):
    return mangayabu.search(search_term)
