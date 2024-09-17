from scrapy.crawler import CrawlerProcess
from crawlers.spiders.google_spider import GoogleSpider


if __name__ == '__main__':
    process = CrawlerProcess()

    process.crawl(GoogleSpider)
    process.start()
