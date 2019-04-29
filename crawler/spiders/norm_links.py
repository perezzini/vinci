import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
import sys

sys.path.append('../') # TODO: correct this. Paths in Python?

import os
import pandas as pd
from stream import DF

class NormLinks(scrapy.Spider):
    name = 'norm_links'

    lua_script = """
                function main(splash)
                  splash.private_mode_enabled = false
                  local url = splash.args.url
                  assert(splash:go(url))
                  assert(splash:wait(0.5))
                  return {
                    html = splash:html(),
                    har = splash:har(),
                  }
                end
                """

    def __init__(self, *args, **kwargs):
        super(NormLinks, self).__init__(*args, **kwargs)
        self.file_path = os.getenv('PROJECT_PATH') + '/' + kwargs.get('file_path', '')  # links of norms to crawl
        self.db_name = kwargs.get('db_name', '')  # where to save crawled norms

    def extract_with_css(self, response, query):
        return response.css(query)

    def start_requests(self):
        df = DF(self.file_path)
        pairs = df.get_rows_by_col_name(col_name=['url', 'fuente'])
        for url, fuente in pairs():
            if fuente == 'saij':
                yield SplashRequest(
                    url=url,
                    callback=self.parse_saij,
                    endpoint='execute',
                    args={
                        'lua_source': self.lua_script
                    },
                    meta={
                        'link': url
                    }
                )
            else:
                if fuente == 'infoleg':
                    yield SplashRequest(
                        url=url,
                        callback=self.parse_infoleg,
                        endpoint='execute',
                        args={
                            'lua_source': self.lua_script
                        },
                        meta={
                            'link': url
                        }
                    )

    def parse_saij(self, response):
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

    def parse_infoleg(self, response):
        full_text = response.xpath('//text()').extract()
        full_text = ' '.join(full_text)

        yield Norm(
            {
                'text': full_text,
                'link': response.meta['link'],
                'html': response.text
            }
        )
