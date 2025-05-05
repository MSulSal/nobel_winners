import scrapy

# define the data to be scraped
class NWinnerItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()


# create a named spider
class NWinnerSpider(scrapy.Spider):
    """ Scrapes the country and link text for Nobel winners. """

    name = "nwinners_list"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"]

    def parse(self, response):
        h3s = response.xpath("//h3")

        for h3 in h3s:
            country = h3.xpath("text()").extract()
            if country:
                winners = h3.xpath("../following-sibling::ol[1]")
                for w in winners.xpath("li"):
                    text = w.xpath("descendant-or-self::text()").extract()
                    link = ''.join(text)
                    yield NWinnerItem(country=country[0], name=text[0], link_text=link)

