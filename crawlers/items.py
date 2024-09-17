import scrapy
from scrapy import Field


class LinkItem(scrapy.Item):
    link = Field()

class PageItem(scrapy.Item):
    source = Field()
    title = Field()
