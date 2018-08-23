# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from database import DB
from datetime import date

class DBPipeline(object):
	def __init__(self):
		self.items = list()

	def open_spider(self, spider):
		self.mongo_client = DB()
		self.collection_name = spider.name

	def close_spider(self, spider):
		document = {
			'date': str(date.today()),
			'data': self.items,
		}
		self.mongo_client.insert_one(self.collection_name, document)
		self.mongo_client.close()
		self.items = list()

	def process_item(self, item, spider):
		self.items.append(dict(item))
		return item
