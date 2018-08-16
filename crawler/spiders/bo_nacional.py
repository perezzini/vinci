import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norma

class BONacional(scrapy.Spider):
    name = 'bo_nacional'
    #allowed_domains = 'boletinoficial.gob.ar' FIXME

    def start_requests(self):
        url = 'https://www.boletinoficial.gob.ar/'
        yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
    	norms = response.css('div#PorCadaNorma')
    	norm_items = norms.css('div.itemsection')
    	norm_urls = norm_items.css('h3 > a::attr(href)').extract()
    	for url in list(norm_urls):
    		url = response.urljoin(url)
    		print(url)
    		yield SplashRequest(url=url, callback=self.parse_details)

    def parse_details(self, response):
    	def extract_with_css(query):
    		return response.css(query).extract_first()

    	full_text = extract_with_css('div#print')
    	soup = BeautifulSoup(full_text, 'html.parser')

    	yield Norma({
			'title': extract_with_css('p.aviso-titulo::text'),
			'abstract': extract_with_css('p.aviso-sintesis::text'),
			'date': extract_with_css('p.aviso-fecha::text'),
    		'full_text': soup.get_text(),
    	})