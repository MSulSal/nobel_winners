import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class NobelImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if info.spider.name != "nwinners_minibio":
            return
        for image_url in item.get("image_urls", []):
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        if info.spider.name != "nwinners_minibio":
            return item
        if not item.get("image_urls"):
            return item
        image_paths = [img["path"] for ok, img in results if ok]

        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter["bio_image"] = image_paths[0]

        return item

class DropNonPersons(object):
    """ Remove non-person winners """

    def process_item(self, item, spider):
        if spider.name != "nwinners_full":
            return item
        if not item.get("gender"):
            raise DropItem("No gender for %s"%item.get("name"))
        return item
