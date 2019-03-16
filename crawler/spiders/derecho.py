import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId
from datetime import date
import textract
import urllib
from utils.misc import iri_to_uri
import time
import sys

class Derecho(scrapy.Spider):
    name = 'derecho'

    lua_script = """
                function main(splash)
                  splash.private_mode_enabled = false
                  local url = splash.args.url
                  assert(splash:go(url))
                  assert(splash:wait(1))
                  return {
                    html = splash:html(),
                    har = splash:har(),
                  }
                end
                """

    def __init__(self, *args, **kwargs):
        super(Derecho, self).__init__(*args, **kwargs)
        self.derecho = kwargs.get('derecho', '')
        self.num_pages = kwargs.get('num_pages', '')
        self.db_name = self.derecho.replace(' ', '_')

    def extract_with_css(self, response, query):
        return response.css(query)

    def start_requests(self):
        def create_start_url():
            root = 'http://www.saij.gob.ar/resultados.jsp?r=tema:'
            concept = self.derecho.replace(' ', '?')
            return root + concept + '&p=' + self.num_pages

        url = create_start_url()
        yield SplashRequest(
            url=url,
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.lua_script
            }
        )

    def parse(self, response):
        norm_urls = self.extract_with_css(response, 'ul.result-list li.result-item div.art-legis-colapsado dd.tit-colapsado a::attr(href)').extract()
        norm_urls = norm_urls[1:]

        for url in norm_urls:
            url = response.urljoin(url)
            yield SplashRequest(
                url=url,
                callback=self.parse_details,
                endpoint='execute',
                args={
                    'lua_source': self.lua_script
                },
                meta={
                    'link': url
                }
            )

    def parse_details(self, response):
        full_text = self.extract_with_css(response, 'div.resultado-busqueda div#div-texto').extract_first()
        full_text = BeautifulSoup(full_text, 'html.parser').get_text()

        abstract = self.extract_with_css(response, 'div.resultado-busqueda div#div-texto div#texto-norma-container').extract_first()
        abstract = BeautifulSoup(abstract, 'html.parser').get_text()
        yield Norm(
            {
                'title': self.extract_with_css(response, 'div.resultado-busqueda li.result-item dd.tit-resultado h1.p-titulo::text').extract_first(),
                'text': full_text,
                'abstract': abstract,
                'link': response.meta['link'],
                'html': response.text
            }
        )
