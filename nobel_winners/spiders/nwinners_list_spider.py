import scrapy


class NwinnersListSpiderSpider(scrapy.Spider):
    name = "nwinners_list_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"]

    def parse(self, response):
        pass
