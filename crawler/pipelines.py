# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from database import DB

class DBPipeline(object):

	def open_spider(self, spider):
		self.mongo_client = DB()
		self.collection_name = spider.name

	def close_spider(self, spider):
		self.mongo_client.close()

	def process_item(self, item, spider):
		self.mongo_client.insert_one(self.collection_name, dict(item))
		return item
