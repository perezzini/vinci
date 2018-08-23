import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Author

class Authors(scrapy.Spider):
    name = 'authors'

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
        url = 'http://quotes.toscrape.com/'
        yield SplashRequest(url=url,
                            callback=self.parse,
                            endpoint='execute',
                            args={
                                    'lua_source': self.lua_script,
                                    'wait': 5,
                                })

    def parse(self, response):
    	urls = response.css('div.quote > span > a::attr(href)').extract()
    	for url in urls:
    		url = response.urljoin(url)
    		yield SplashRequest(url=url,
                                callback=self.parse_details,
                                endpoint='execute',
                                args={
                                    'lua_source': self.lua_script,
                                    'wait': 5,
                                })

    def parse_details(self, response):
        container = response.css('div.author-details').extract_first()
        soup = BeautifulSoup(container, 'html.parser')
        return Author({
            'description': soup.get_text()
        })