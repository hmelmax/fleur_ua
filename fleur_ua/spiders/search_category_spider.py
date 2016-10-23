import scrapy
import math

from fleur_ua.items import FleurUaCategory

class SearchCategorySpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        self.name = "search_category_spider"
        super(SearchCategorySpider, self).__init__(*args, **kwargs)

        self.start_urls = ["http://fleur.ua/parfyumeriya.html"]

    def parse(self, response):
        for url in response.xpath('//div[@class="mob-hide"]/ul/li/a/@href'):
            item = FleurUaCategory()
            item["name"] = url.extract().split("/")[-1].split(".")[0]
            item["url"] = url.extract()
            yield scrapy.Request(url=item["url"], meta={"item": item}, callback=self.parse_pages)

    def parse_pages(self, response):
        all_product = response.xpath('//div[@class="total"]/text()').extract()[0].split()[0].encode("utf-8")
        item = response.meta["item"]
        item["page_count"] = int(math.ceil(int(all_product) / 60.0))
        yield item



