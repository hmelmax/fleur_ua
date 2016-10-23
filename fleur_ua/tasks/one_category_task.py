from taskflow import task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from fleur_ua.spiders.one_category_spider import OneCategorySpider


class OneCategoryTask(task.Task):

    def __init__(self, category_name, page):
        self.category_name = category_name
        self.page = page
        super(OneCategoryTask, self).__init__(name=category_name+str(page), inject=None)
    def execute(self):
        settings = get_project_settings()
        category_process = CrawlerProcess(settings)
        category_process.crawl(OneCategorySpider, name=self.category_name, page=self.page)
        category_process.start()
        category_process.join()

