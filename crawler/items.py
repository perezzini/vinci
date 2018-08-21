# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Author(scrapy.Item):
	description = scrapy.Field()

class Norma(scrapy.Item):
	full_text = scrapy.Field()
	type = scrapy.Field()

	def get_type_of_norm(txt):
			txt = txt.lower()

			if 'decreto' in txt:
				return 'd'
			elif 'aviso' in txt:
				return 'a'
			elif 'convocatoria' in txt:
				return 'c'
			elif 'contrato' in txt:
				return 'cont'
			elif 'remate' in txt:
				return 'rem'
			elif 'edictos' in txt:
				return 'e'
			elif 'resolucion' in txt:
				return 'r'
			elif 'resolucion general' in txt:
				return 'rg'
			elif 'resolucion sintetizada' in txt:
				return 'rs'
			elif 'disposicion' in txt:
				return 'disp'
			elif 'ley' in txt:
				return 'l'
			elif 'decision administrativa' in txt:
				return 'da'
			elif 'ordenanza' in txt:
				return 'o'
			else:
				return 'None'

class NormaNacional(Norma):
	title = scrapy.Field()
	abstract = scrapy.Field()
	date = scrapy.Field()
	full_type = scrapy.Field()
	published_date = scrapy.Field()
	anexos = scrapy.Field()

class NormaSantaFe(Norma):
	pass