from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Spider():
    def __init__(self, name):
        self.spider = name
        self.process =  CrawlerProcess(get_project_settings())

    def crawl(self):
        self.process.crawl(self.spider)
        self.process.start()  # the script will block here until the crawling is finished

    def stop(self):
        self.process.stop()
