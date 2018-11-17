import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId

from datetime import date

class BONacional(scrapy.Spider):
	name = 'bo_nacional'
	#allowed_domains = 'boletinoficial.gob.ar' FIXME

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
				"""  # TODO: must better understand this. Note that splash.private_mode_enabled = true

	def start_requests(self):
		url = 'https://www.boletinoficial.gob.ar/'
		yield SplashRequest(url=url,
							callback=self.parse,
							endpoint='execute',
							args={
									'lua_source': self.lua_script,
									'wait': 5,
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
									'wait': 5,
								})

	def parse_details(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first()

		full_text = extract_with_css('div.item')
		soup = BeautifulSoup(full_text, 'html.parser')

		if extract_with_css('p.aviso-norma::text'):
			type = Norm.get_type_of_norm(extract_with_css('p.aviso-norma::text'))
		else:
			type = None

		if response.css('div#anexos a::attr(href)'):
			annexes = list(map(lambda url: response.urljoin(url), response.css('div#anexos a::attr(href)').extract()))
		else:
			annexes = None

		yield Norm({
			'published_at': str(date.today()),
			'title': extract_with_css('p.aviso-titulo::text'),
			'abstract': extract_with_css('p.aviso-sintesis::text'),
			'text': soup.get_text(),
			'type': dict(simple=type,
						full_text=extract_with_css('p.aviso-norma::text')),
			'annexes': annexes
		})
