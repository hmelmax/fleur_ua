import scrapy


class FleurUaItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    sku = scrapy.Field()
    available = scrapy.Field()


class FleurUaCategory(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    page_count = scrapy.Field()
    last_page = scrapy.Field()

