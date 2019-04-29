import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId
import os
from datetime import date

class BONacionalDaily(scrapy.Spider):
	name = 'bo_nacional_daily'

	db_name = 'bo_nacional_daily'

	lua_script = """
				function main(splash)
				  splash.private_mode_enabled = true
				  local url = splash.args.url
				  assert(splash:go(url))
				  assert(splash:wait(0.5))
				  return {
				    html = splash:html(),
				    har = splash:har(),
				  }
				end
				"""  # TODO: must better understand this. Note that splash.private_mode_enabled = true

	def extract_with_css(self, response, query):
		return response.css(query)

	def start_requests(self):
		url = os.getenv('BO_NACIONAL')
		yield SplashRequest(url=url,
							callback=self.parse,
							endpoint='execute',
							args={
									'lua_source': self.lua_script,
								},
							meta={
								'date': date.today().strftime('%Y-%m-%d')
							})

	def parse(self, response):
		norm_urls = response.css('div#avisosSeccionDiv a::attr(href)').extract()

		for url in norm_urls:
			if 'anexo' not in url:
				url = response.urljoin(url)
				yield SplashRequest(url=url,
									callback=self.parse_details,
									endpoint='execute',
									args={
										'lua_source': self.lua_script,
									},
									meta={
										'link': url,
										'date': response.meta['date']
									})

	def parse_details(self, response):
		full_text = self.extract_with_css(response, 'div.avisoContenido div#detalleAviso').extract_first()
		full_text_soup = BeautifulSoup(full_text, 'html.parser')

		title = self.extract_with_css(response, 'div.avisoContenido div#detalleAviso div#tituloDetalleAviso').extract_first()
		title_soup = BeautifulSoup(title, 'html.parser')


		if self.extract_with_css(response, 'div.avisoContenido div#detalleAviso div#tituloDetalleAviso').extract_first():
			simple_type = Norm.get_type_from_text(self.extract_with_css(response, 'div.avisoContenido div#detalleAviso div#tituloDetalleAviso').extract_first())
		else:
			simple_type = None

		yield Norm({
			'published_at': response.meta['date'],
			'title': title_soup.get_text(),
			'text': full_text_soup.get_text(),
			'type': dict(simple=simple_type),
			'link': response.meta['link'],
			'html': response.text
		})
