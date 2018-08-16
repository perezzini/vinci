import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Author

class Authors(scrapy.Spider):
    name = 'authors'

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
        soup = BeautifulSoup(container, 'html.parser')
        yield Author({
            'description': soup.get_text()
        })