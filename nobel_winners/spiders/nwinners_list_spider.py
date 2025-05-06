import scrapy
import re

BASE_URL = "http://en.wikipedia.org"

def process_winner_li(w, country=None):
    """
    Process a winner's <li> tag, adding country of birth or nationality,
    as applicable.
    """
    wdata = {}
    wdata["link"] = BASE_URL + w.xpath("a/@href").extract()[0]

    text = "".join(w.xpath("descendant-or-self::text()").extract())
    wdata["name"] = text.split(",")[0].strip()

    year = re.findall("\d{4}", text)

    if year:
        wdata["year"] = int(year[0])
    else:
        wdata["year"] = 0
        print("Oops, no year in", text)

    category = re.findall(
        "Physics|Chemistry|Physiology or Medicine|Literature|Peace|Economics",
        text
    )

    if category:
        wdata["category"] = category[0]
    else:
        wdata["category"] = ""
        print("Oops, no category in", text)

    if country:
        if text.find("*") != -1:
            wdata["country"] = ""
            wdata["born_in"] = country
        else:
            wdata["country"] = country
            wdata["born_in"] = ""

    wdata["text"] = text
    return wdata

# define the data to be scraped
class NWinnerItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    country = scrapy.Field()
    # gender = scrapy.Field()
    # born_in = scrapy.Field()
    # date_of_birth = scrapy.Field()
    # data_of_death = scrapy.Field()
    # place_of_birth = scrapy.Field()
    # place_of_death = scrapy.Field()
    # text = scrapy.Field()


# create a named spider
class NWinnerSpider(scrapy.Spider):
    """ Scrapes the country and link text for Nobel winners. """

    name = "nwinners_list"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"]

    def parse(self, response):
        h3s = response.xpath("//h3")

        for h3 in h3s:
            country = h3.xpath("text()").extract()[0]
            if country:
                winners = h3.xpath("../following-sibling::ol[1]")
                for w in winners.xpath("li"):
                    wdata = process_winner_li(w, country)
                    yield NWinnerItem(
                        name=wdata["name"],
                        link=wdata["link"],
                        year=wdata["year"],
                        country=wdata["country"],
                        category=wdata["category"]
                    )

