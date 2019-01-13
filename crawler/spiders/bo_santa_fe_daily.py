import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
import utils
from bson.objectid import ObjectId
from datetime import date
import re
import os

class BOSantaFeDaily(scrapy.Spider):
	name = 'bo_santa_fe_daily'

	lua_script = """
                function main(splash)
                  splash.private_mode_enabled = true
                  local url = splash.args.url
                  assert(splash:go(url))
                  assert(splash:wait(1))
                  return {
                    html = splash:html(),
                    har = splash:har(),
                  }
                end
                """  # TODO: must better understand this...

	def start_requests(self):
		url = os.getenv('BO_PROVINCIAL') + 'resumendia.php?pdia=ultimo&dia=' + date.today().strftime('%Y-%m-%d')
		yield SplashRequest(url=url,
							callback=self.parse,
							endpoint='execute',
							args={
								'lua_source': self.lua_script,
							})

	def parse(self, response):
		def extract_with_css(query):
			return response.css(query)
		urls = extract_with_css('a::attr(href)').re(r'ver.*')  # TODO: check expression
		urls = list(map(response.urljoin, urls))

		for url in urls:
			yield SplashRequest(url=url,
								callback=self.parse_details,
								endpoint='execute',
								args={
									'lua_source': self.lua_script,
								},
								meta={
									'link': url,
									'type': Norm.get_type_from_text(url),
								})

	def parse_details(self, response):
		def extract_with_css(query):
			return response.css(query)

		content = extract_with_css('p.western').extract()
		content = ''.join(content)

		soup = BeautifulSoup(content, 'html.parser')

		yield Norm({
			'published_at': date.today().strftime('%Y-%m-%d'),
			'text': soup.get_text(),
			'type': dict(simple=response.meta['type']),
			'link': response.meta['link'],
			'html': response.text
		})
