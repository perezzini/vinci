import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import NormaSantaFe
import utils

class BOSantaFe(scrapy.Spider):
	name = 'bo_santa_fe'

	lua_script = """
                function main(splash)
                  splash.private_mode_enabled = true
                  local url = splash.args.url
                  assert(splash:go(url))
                  assert(splash:wait(10))
                  return {
                    html = splash:html(),
                    har = splash:har(),
                  }
                end
                """  # TODO: must better understand this...

	def start_requests(self):
		url = 'https://www.santafe.gob.ar/boletinoficial/'
		yield SplashRequest(url=url,
							callback=self.parse,
							endpoint='execute',
							args={
								'lua_source': self.lua_script,
								'wait': 5,
							})

	def parse(self, response):
		def extract_with_css(query):
			return response.css(query)

		url = extract_with_css('a.link::attr(href)').extract_first()  # TODO: check expression
		url = response.urljoin(url)

		yield SplashRequest(url=url,
							callback=self.parse_norms,
							endpoint='execute',
							args={
								'lua_source': self.lua_script,
								'wait': 5,
							})

	def parse_norms(self, response):
		def extract_with_css(query):
			return response.css(query)

		urls = extract_with_css('tr.texto_resumen_BO a::attr(href)').extract()  # TODO: check expressions

		for url in urls:
			yield SplashRequest(url=url,
								callback=self.parse_details,
								meta={
									'type': NormaSantaFe.get_type_of_norm(url),
								},
								endpoint='execute',
								args={
									'lua_source': self.lua_script,
									'wait': 5,
								})

	def parse_details(self, response):
		def extract_with_css(query):
			return response.css(query)

		html = extract_with_css('body').extract_first()

		full_text = BeautifulSoup(html, 'html.parser').get_text()

		lines = full_text.splitlines()  # List of HTML text lines

		norms = utils.split_list_by_sep(lines, '__________________________________________')

		norms = list(map(lambda l: [' '.join(l)], norms))  # A list of separated norms

		for norm in norms:
			yield NormaSantaFe({
					'full_text': norm[0],
					'type': response.meta['type'],
				})
