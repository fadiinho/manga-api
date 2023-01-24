import requests


class BaseScraper:
    def __init__(self, base_host):
        self.base_host = base_host
        self.client = requests.session()
