import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId

from datetime import date
import utils

class BOSantaFe(scrapy.Spider):
	name = 'bo_santa_fe_all'

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
		dates = utils.gen_all_dates('05/03/2002', '11/16/2018')
		root_url = 'https://www.santafe.gob.ar/boletinoficial/resumendia.php?pdia=ultimo&dia='
		urls_dates = ((root_url + date, date) for date in dates)
		for url, date in urls_dates:
			yield SplashRequest(url=url,
								callback=self.parse_norms,
								endpoint='execute',
								args={
									'lua_source': self.lua_script,
									'wait': 5,
								},
								meta={
									'date': date
								})

	def parse_norms(self, response):
		def extract_with_css(query):
			return response.css(query)

		urls = extract_with_css('tr.texto_resumen_BO a::attr(href)').extract()  # TODO: check expressions

		for url in urls:
			yield SplashRequest(url=url,
								callback=self.parse_details,
								meta={
									'type': Norm.get_type_of_norm(url),
									'date': response.meta['date']
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

		norms = utils.split_list_by_sep(lines, '__')

		norms = list(map(lambda l: [' '.join(l)], norms))  # A list of separated norms from the same source

		for norm in norms:
			yield Norm({
				'published_at': response.meta['date'],
				'text': norm[0],
				'type': dict(simple=response.meta['type'])
			})
