import scrapy

from fleur_ua.items import FleurUaItem

class OneCategorySpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        self.page = kwargs.get("page")
        super(OneCategorySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://fleur.ua/parfyumeriya/%s.html?dir=asc&limit=60&order=custom_bestseller_sort&p=%s' % (self.name, self.page)]



    def parse(self, response):
        for href in response.xpath('//ul[@class="products-grid"]/li/a[starts-with(@href, "http://fleur.ua/")]/@href'):
            yield scrapy.Request(href.extract(), callback=self.parse_item_content)

    def parse_item_content(self, response):

        for product in response.xpath('//div[@class="ham"]'):
            item = FleurUaItem()
            try:
                first_name = response.xpath('//div[@class="product-name"]/a/text()').extract()[0]
                item["name"] = first_name + " " + product.xpath('//h1[@class="product-name"]/text()').extract()[0]
                item["sku"] = int(product.xpath('@id').extract()[0])
                category = []
                for subcategory in response.xpath('//div[@class="breadcrumbs"]/ul/li/a/text()'):
                    category.append(subcategory.extract())
                item["category"] = ">".join(category)
                price = product.xpath('//span[@id="product-price-%s"]/span/text()' % item["sku"]).extract()
                if len(price) > 0:
                    item["price"] = int(price[0].replace(u'\xa0', u''))
                else:
                    item["price"] = 0
                item["available"] = product.xpath('//p[@class="availability in-stock"]/span/text()').extract()[0]
            except:
                pass
            yield item
