# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from database import DB
from datetime import date

class AuthorPipeline(object):
	collection_name = 'authors'

	def __init__(self):
		self.mongo_client = DB()
		self.db = self.mongo_client.import_db('test')

		self.items = list()

	def close_spider(self, spider):
		document = {
			'date': str(date.today()),
			'authors': list(map(lambda a: dict(a), self.items))
		}
		self.mongo_client.insert_one(self.collection_name, document)
		self.mongo_client.close()

	def process_item(self, item, spider):
		self.items.append(item)
		return item

class BONacionalPipeline(object):
	collection_name = 'bo_nacional'

	def __init__(self):
		self.mongo_client = DB()
		self.db = self.mongo_client.import_db('test')

		self.items = list()

	def close_spider(self, spider):
		document = {
			'date': str(date.today()),
			'norms': list(map(lambda n: dict(n), self.items))
		}
		self.mongo_client.insert_one(self.collection_name, document)
		self.mongo_client.close()

	def process_item(self, item, spider):
		self.items.append(item)
		return item
