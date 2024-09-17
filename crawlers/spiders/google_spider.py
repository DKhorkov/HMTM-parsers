import random
from typing import List
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
import json
from datetime import datetime

from crawlers.items import LinkItem


def create_google_url(query, site=''):
   google_dict = {'q': query, 'num': 100, 'start': 0}
   if site:
       web = urlparse(site).netloc
       google_dict['as_sitesearch'] = web
       return 'http://www.google.com/search?' + urlencode(google_dict)
   return 'http://www.google.com/search?' + urlencode(google_dict)


def load_proxy() -> list[str]:
    with open('proxylist.txt', 'r') as f:
        return [proxy for proxy in f.read().splitlines()]


def load_queries() -> list[str]:
    with open('search_engine_queries.txt', 'r') as f:
        return [query for query in f.read().splitlines()]


class GoogleSpider(scrapy.Spider):
   name = 'google_spider'
   allowed_domains = ['google.com']
   custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10
   }

   def start_requests(self):
       proxies: List[str] = load_proxy()
       queries: List[str] = load_queries()

       for query in queries:
           url = create_google_url(query)
           print(url)
           random_proxy = random.choice(proxies)
           yield scrapy.Request(
               url=url,
               callback=self.parse,
               meta={'pos': 0}
           )

   def parse(self, response):
       print(response.url)
       for element in response.xpath("//a"):
           item = LinkItem()
           print(element, 'element')
           oglink = element.xpath("@href").extract()
           print(oglink, 'og link')

       return
