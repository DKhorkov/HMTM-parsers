from abc import ABC, abstractmethod
from typing import Iterator
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


class QueryBuilder(ABC):
    domain: str
    num: int

    def __init__(self, start_queries: list[str]):
        self.start_queries = start_queries
        self.query_urls: set[str] = set()
        self._start = None

    @abstractmethod
    def create_url(self, query: str) -> str:
        pass

    @property
    def start(self) -> int:
        return self._start

    @start.setter
    def start(self, shift: int) -> None:
        self._start = shift

    def start_urls(self) -> Iterator[str]:
        for query in self.start_queries:
            yield self.create_url(query)


class GoogleQueryBuilder(QueryBuilder):
    domain: str = "http://www.google.com/search?"
    num: int = 100

    def create_url(self, query: str) -> str:
        q_params = {'q': query, 'num': self.num, 'start': self.start}
        return self.domain + urlencode(q_params)


class YandexQueryBuilder(QueryBuilder):
    def create_url(self, query: str):
        pass


class PageProcessor(ABC):
    @abstractmethod
    def parse(self, page: str):
        pass


class GooglePageProcessor(PageProcessor):
    pass


class YandexPageProcessor(PageProcessor):
    pass


class ParsingMachine:
    def __init__(self, query_builder: QueryBuilder, page_processor: PageProcessor):
        self.qbuilder = query_builder
        self.page_processor = page_processor

    def process_engine(self):
        while self.qbuilder.query_urls:
            curr_url: str = self.qbuilder.query_urls.pop()
            res = requests.get(url=curr_url, proxies=gen_proxy())
            if res.status_code != 200:
                print(res.status_code)


if __name__ == "__main__":
    target_urls: set[str] = set()

    qbuilder = GoogleQueryBuilder(
        start_queries=start_queries
    )
    pp = GooglePageProcessor()
    pm = ParsingMachine(qbuilder, pp)

    while target_urls:
        pass
