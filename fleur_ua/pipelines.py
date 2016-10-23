from fleur_ua.db import DB


class FleurUaPipeline(object):

    def __init__(self, *args, **kwargs):
        self.db = DB()
        super(FleurUaPipeline, self).__init__(*args, **kwargs)

    def open_spider(self, spider):
        self.db.connect()
        if spider.name == "search_category_spider":
            self.db.create_if_empty()

    def close_spider(self, spider):
        if spider.name == "search_category_spider":
            self.db.swap()
        else:
            self.db.update_category(spider.name, spider.page)
        self.db.disconnect()

    def process_item(self, item, spider):
        if spider.name == "search_category_spider":
            self.db.insert_into_category(item["name"], item["url"], item["page_count"])
        else:
            self.db.insert_into_tmp_item(item["name"], item["price"], item["category"], item["sku"], item["available"])
        return item

