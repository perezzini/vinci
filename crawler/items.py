# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Author(scrapy.Item):
	description = scrapy.Field()

class Norm(scrapy.Item):
	published_at = scrapy.Field()
	title = scrapy.Field()
	abstract = scrapy.Field()
	annexes = scrapy.Field()
	text = scrapy.Field()
	type = scrapy.Field()
	link = scrapy.Field()
	html = scrapy.Field()

	# TODO: re-design this
	def get_type_from_text(txt):
			txt = txt.lower()

			if 'decreto' in txt:
				return 'decreto'
			elif 'aviso' in txt:
				return 'aviso'
			elif 'convocatoria' in txt:
				return 'convocatoria'
			elif 'contrato' in txt:
				return 'contrato'
			elif 'remate' in txt:
				return 'remate'
			elif 'edicto' in txt:
				return 'edicto'
			elif 'resolucion' in txt:
				return 'resolucion'
			elif 'resolucion general' in txt:
				return 'resolucion general'
			elif 'resolucion sintetizada' in txt:
				return 'resolucion sintetizada'
			elif 'disposicion' in txt:
				return 'disposicion'
			elif 'ley' in txt:
				return 'ley'
			elif 'decision administrativa' in txt:
				return 'decision administrativa'
			elif 'ordenanza' in txt:
				return 'ordenanza'
			elif 'licitacion' in txt:
				return 'licitacion'
			else:
				return 'None'
