import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId
import os
from datetime import date

class BONacionalDaily(scrapy.Spider):
	name = 'bo_nacional_daily'

	lua_script = """
				function main(splash)
				  splash.private_mode_enabled = true
				  local url = splash.args.url
				  assert(splash:go(url))
				  assert(splash:wait(5))
				  return {
				    html = splash:html(),
				    har = splash:har(),
				  }
				end
				"""  # TODO: must better understand this. Note that splash.private_mode_enabled = true

	def start_requests(self):
		url = os.getenv('BO_NACIONAL')
		yield SplashRequest(url=url,
							callback=self.parse,
							endpoint='execute',
							args={
									'lua_source': self.lua_script,
								})

	def parse(self, response):
		norms = response.css('div#PorCadaNorma')
		norm_items = norms.css('div.itemsection')
		norm_urls = norm_items.css('h3 > a::attr(href)').extract()

		for url in list(norm_urls):
			url = response.urljoin(url)
			yield SplashRequest(url=url,
								callback=self.parse_details,
								endpoint='execute',
								args={
									'lua_source': self.lua_script,
								},
								meta={
									'link': url,
								})

	def parse_details(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first()

		full_text = extract_with_css('div.item')
		soup = BeautifulSoup(full_text, 'html.parser')

		if extract_with_css('p.aviso-norma::text'):
			type = Norm.get_type_from_text(extract_with_css('p.aviso-norma::text'))
		else:
			type = None

		if response.css('div#anexos a::attr(href)'):
			annexes = list(map(lambda url: response.urljoin(url), response.css('div#anexos a::attr(href)').extract()))
		else:
			annexes = None

		yield Norm({
			'published_at': date.today().strftime('%Y-%m-%d'),
			'title': extract_with_css('p.aviso-titulo::text'),
			'abstract': extract_with_css('p.aviso-sintesis::text'),
			'text': soup.get_text(),
			'type': dict(simple=type,
						full=extract_with_css('p.aviso-norma::text')),
			'annexes': annexes,
			'link': response.meta['link'],
			'html': response.text
		})
