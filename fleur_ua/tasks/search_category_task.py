from taskflow import task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from fleur_ua.spiders.search_category_spider import SearchCategorySpider



class SearchCategoryTask(task.Task):
    def __init__(self):
        super(SearchCategoryTask, self).__init__()

    def execute(self):
        settings = get_project_settings()
        search_category_process = CrawlerProcess(settings)
        search_category_process.crawl(SearchCategorySpider)
        search_category_process.start()
        search_category_process.join()

