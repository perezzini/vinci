import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId
from datetime import date
import textract
import urllib
from utils import iri_to_uri
import time
import sys

class BOSanLorenzoAll(scrapy.Spider):
    name = 'bo_san_lorenzo_all'

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
                """

    def extract_with_css(self, response, query):
        return response.css(query)

    def start_requests(self):
        sys.path.append('../') # TODO: correct this. Paths in Python?

        pages = list(range(1, 85))
        root_url = 'http://sanlorenzo.gob.ar/ordenanzas/page/'
        urls = list(map(lambda p: root_url + str(p), pages))
        for url in urls:
            yield SplashRequest(
                url=url,
                callback=self.parse_list,
                endpoint='execute',
                args={
                    'lua_source': self.lua_script,
                }
            )

    def parse_list(self, response):
        urls = self.extract_with_css(response, 'div.posts-container article a.more-link::attr(href)').extract()
        for url in urls:
            yield SplashRequest(
                url=url,
                callback=self.parse_norm,
                endpoint='execute',
                args={
                    'lua_source': self.lua_script,
                },
                meta={
                    'link': url
                }
            )

    def parse_norm(self, response):
        # print('Entered parse_norm')
        published_at = self.extract_with_css(response, 'span.meta-date::text').extract_first()
        type = self.extract_with_css(response, 'div.main-content h1.entry-title::text').extract_first()
        pdf_link = self.extract_with_css(response, 'p.embed_download a::attr(href)')
        if len(pdf_link) == 1:
            # extract text from PDF
            # print('\nExtract text from PDF...')
            res_name = '../ext_data/normatives/municipal/san-lorenzo/datasets/pdf/' + response.meta['link'].rsplit('/', 2)[-2] + '.pdf'
            # print('res_name', res_name)
            pdf_name = pdf_link.extract_first()
            pdf_name = iri_to_uri(pdf_name)
            # print('pdf_name', pdf_name)
            urllib.request.urlretrieve(pdf_name, res_name)
            text = textract.process(res_name).decode("utf-8")
            # print('Done!\n')

        else:
            # extract plain-text
            # print('\nExtract text from HTML...')
            html = self.extract_with_css(response, 'div.main-content').extract_first()
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            # print('Done!\n')
        yield Norm(
            {
                'published_at': published_at,
                'type': dict(full=type),
                'text': text,
                'link': response.meta['link'],
                'html': response.text
            }
        )
        print('Finished parse_norm')
