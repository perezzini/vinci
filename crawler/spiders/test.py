import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

class Test(scrapy.Spider):
	name = 'test'

	lua_script = """
	function main(splash)
  splash.private_mode_enabled = false
  local url = splash.args.url
  assert(splash:go(url))
  assert(splash:wait(10))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""

	def start_requests(self):
		url = 'https://www.boletinoficial.gob.ar/#!DetalleNorma/190173/20180821'
		yield SplashRequest(url=url, 
							callback=self.parse,
							endpoint='execute',
							args={
								'lua_source': self.lua_script,
							})

	def parse(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first()

		full_text = extract_with_css('div.item')
		soup = BeautifulSoup(full_text, 'html.parser')
		yield {
			'titulo': extract_with_css('p.aviso-titulo::text'),
			'full_text': soup.get_text(),
		}