import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

class Quotes(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
    	urls = response.css('div.quote > span > a::attr(href)').extract()
    	for url in urls:
    		url = response.urljoin(url)
    		yield SplashRequest(url=url, callback=self.parse_details)

    def parse_details(self, response):
        container = response.css('div.author-details').extract_first()
        soup = BeautifulSoup(container)
        yield {
            'complete': soup.get_text()
        }