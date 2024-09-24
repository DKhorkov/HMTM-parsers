from abc import ABC, abstractmethod
from typing import Any
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import requests
from fp.fp import FreeProxy

start_queries = [
    "мягкие игрушки",
    "мастер мягкие игрушки",
    "мягкие игрушки производство",
    "мягкие игрушки ручной работы",
    "валяные игрушки"
]


def gen_proxy():
    return {
        "http": FreeProxy(google=True).get()
    }


def request_content(url: str) -> bytes:
    res = requests.get(url=url, proxies=gen_proxy())
    if res.status_code == 200:
        return res.content

    print("Content doesnt load", res.status_code)
    raise Exception(res.status_code)


class EngineParser(ABC):
    def __init__(self, start_queries: list[str]):
        self.seen: set[str] = set()
        self.urls: set[str] = set()

        def start_urls() -> None:
            for query in start_queries:
                self.urls.add(self.create_url(query))

            self.seen = self.urls

        start_urls()

    @abstractmethod
    def create_url(self, query: str) -> str:
        pass

    def search(self, url: str) -> Any:
        pass


class GoogleParser(EngineParser):
    domain: str = "http://www.google.com/search?"
    num: int = 100
    headers_get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    item_xpath = "/html/body/div[3]/div/div[13]/div[2]/div[1]/div[2]/div/div/div[11]/div/div/div[1]/div/div/span/a/div/div/div/div[2]/cite"
    pagination_xpath = ""

    def create_url(self, query: str) -> str:
        q_params = {'q': query, 'num': self.num}
        return self.domain + urlencode(q_params)

    def search(self, url: str) -> Any:
        s = requests.Session()
        r = s.get(url, headers=self.headers_get, proxies=gen_proxy())
        soup = BeautifulSoup(r.text, "html.parser")
        for item in soup.find_all('cite'):
            print(item)
            # target_url = searchWrapper.find('a')["href"]
            # pagination = searchWrapper.find('a').text.strip()


class YandexParser(EngineParser):
    def create_url(self, query: str):
        pass


if __name__ == "__main__":
    target_urls: set[str] = set()
    # Set engine parser
    # build start engine defined queries
    parser = GoogleParser(start_queries=start_queries)

    # start requests through queries before empty set()
    while parser.urls:
        url = parser.urls.pop()
        parser.search(url)

    #     # process query result engine page
    #     # collect target urls
    #     # add new query urls prom paginatio
