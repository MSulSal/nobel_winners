from scrapy.exceptions import DropItem

class DropNonPersons(object):
    """ Remove non-person winners """

    def process_item(self, item, spider):
        if not item["gender"]:
            raise DropItem("No gender for %s"%item["name"])
        return item
