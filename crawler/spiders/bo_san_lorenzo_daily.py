import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from crawler.items import Norm
from bson.objectid import ObjectId
from datetime import date
import textract
import urllib
from utils.misc import iri_to_uri
from dateutil import parser
import os

class BOSanLorenzoDaily(scrapy.Spider):
    name = 'bo_san_lorenzo_daily'

    db_name = 'bo_san_lorenzo_daily'

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
        url = os.getenv('BO_MUNICIPAL')
        today = date.today().strftime('%Y-%m-%d')
        yield SplashRequest(
            url=url,
            callback=self.parse_list,
            endpoint='execute',
            args={
                'lua_source': self.lua_script,
            },
            meta={
                'today': today
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
                    'link': url,
                    'today': response.meta['today']
                }
            )

    def parse_norm(self, response):
        meta_date = self.extract_with_css(response, 'span.meta-date::text').extract_first()
        today = date.today().strftime('%Y-%m-%d')
        # print(meta_date)
        def date_from_en_to_es(m):
            split = m.split()
            def translate(arg):
                arg = arg.lower()
                if arg == 'enero':
                    return 'jan'
                elif arg == 'febrero':
                    return 'feb'
                elif arg == 'marzo':
                    return 'mar'
                elif arg == 'abril':
                    return 'apr'
                elif arg == 'mayo':
                    return 'may'
                elif arg == 'junio':
                    return 'jun'
                elif arg == 'julio':
                    return 'jul'
                elif arg == 'agosto':
                    return 'aug'
                elif (arg == 'septiembre') | (arg == 'setiembre'):
                    return 'sep'
                elif arg == 'octubre':
                    return 'oct'
                elif arg == 'noviembre':
                    return 'nov'
                elif arg == 'diciembre':
                    return 'dec'
                else:
                    return 'None'

            split[0] = translate(split[0])
            date = ' '.join(split)
            return date

        meta_date = parser.parse(date_from_en_to_es(meta_date))
        meta_date = meta_date.strftime('%Y-%m-%d')
        # print(meta_date)

        if meta_date == today:
            # crawl new norm
            # print('Entered parse_norm')
            type = self.extract_with_css(response, 'div.main-content h1.entry-title::text').extract_first()
            pdf_link = self.extract_with_css(response, 'p.embed_download a::attr(href)')

            if len(pdf_link) == 1:
                # extract text from PDF
                # print('\nExtract text from PDF...')
                res_name = os.getenv('NORMATIVES_MUNICIPAL_PATH') + '/datasets/pdf/' + response.meta['link'].rsplit('/', 2)[-2] + '.pdf'
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
                    'published_at': meta_date,
                    'type': dict(full=type),
                    'text': text,
                    'link': response.meta['link'],
                    'html': response.text
                }
            )
