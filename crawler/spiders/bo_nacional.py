import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

class BONacional(scrapy.Spider):
    name = "bo_nacional"

    def start_requests(self):
        url = 'https://www.boletinoficial.gob.ar/'
        yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
    	print('========== PARSING =========')
    	print(response.text)
    	print('========== END PARSING =========')
    	norms = response.css('div#PorCadaNorma')
    	norm_items = norms.css('div.itemsection')
    	norm_urls = norm_items.css('h3 > a::attr(href)').extract()
    	for url in list(norm_urls):
    		url = response.urljoin(url)
    		print(url)
    		yield SplashRequest(url=url, callback=self.parse_details)

    def parse_details(self, response):
    	full_text = response.css('div#print').extract_first()
    	soup = BeautifulSoup(full_text, 'html.parser')
    	yield {
    		'structured': {
    			'titulo': response.css('p.aviso-titulo::text').extract_first(),
    			'sintesis': response.css('p.aviso-sintesis::text').extract_first(),
    			'fecha': response.css('p.aviso-fecha::text').extract_first(),
    		},
    		'full-text': soup.get_text(),
    	}