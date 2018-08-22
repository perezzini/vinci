import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId

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

		norm = Norm()
		for url in list(norm_urls):
			url = response.urljoin(url)
			yield SplashRequest(url=url,
								callback=self.parse_details,
								endpoint='execute',
								args={
									'lua_source': self.lua_script,
									'wait': 5,
								},
								meta={
									'norm': norm
								})

	def parse_details(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first()

		norm = response.meta['norm']

		full_text = extract_with_css('div.item')
		soup = BeautifulSoup(full_text, 'html.parser')

		if extract_with_css('p.aviso-norma::text'):
			type = Norm.get_type_of_norm(extract_with_css('p.aviso-norma::text'))
		else:
			type = None

		if response.css('div#anexos a::attr(href)'):
			anexos = list(map(lambda url: response.urljoin(url), response.css('div#anexos a::attr(href)').extract()))
		else:
			anexos = None

		norm['_id'] = ObjectId()
		norm['title'] = extract_with_css('p.aviso-titulo::text')
		norm['abstract'] = extract_with_css('p.aviso-sintesis::text')
		norm['date'] = extract_with_css('p.aviso-fecha::text')
		norm['full_text'] = soup.get_text()
		norm['type'] = dict(simple=type,
							full_text=extract_with_css('p.aviso-norma::text'))
		norm['anexos'] = anexos

		return norm
