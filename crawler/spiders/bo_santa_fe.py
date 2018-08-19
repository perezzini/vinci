import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norma
import utils

class BOSantaFe(scrapy.Spider):
	name = 'bo_santa_fe'
	#allowed_domains = 'boletinoficial.gob.ar' FIXME

	def start_requests(self):
		url = 'https://www.santafe.gob.ar/boletinoficial/'
		yield SplashRequest(url=url, callback=self.parse)

	def parse(self, response):
		def extract_with_css(query):
			return response.css(query)

		url = extract_with_css('a.link::attr(href)').extract_first()  # TODO: check expression
		url = response.urljoin(url)

		yield SplashRequest(url=url, callback=self.parse_norms)

	def parse_norms(self, response):
		def extract_with_css(query):
			return response.css(query)

		urls = extract_with_css('tr.texto_resumen_BO a::attr(href)').extract()  # TODO: check expressions

		for url in urls:
			yield SplashRequest(url=url, callback=self.parse_details, meta={'type': Norma.get_type_of_norm(url)})

	def parse_details(self, response):
		def extract_with_css(query):
			return response.css(query)

		html = extract_with_css('body').extract_first()

		full_text = BeautifulSoup(html, 'html.parser').get_text()

		lines = full_text.splitlines()  # List of HTML text lines

		norms = utils.split_list_by_sep(lines, '__________________________________________')

		norms = list(map(lambda l: [' '.join(l)], norms))  # A list of separated norms

		for norm in norms:
			yield Norma({
					'full_text': norm[0],
					'type': response.meta['type'],
				})
