import pymongo
import settings

class DB():
	def __init__(self):
		self.client = pymongo.MongoClient(settings.DB_SERVER, int(settings.DB_PORT))  # Connect to client

	def close(self):
		self.client.close()

	def import_db(self, db):
		self.db = self.client[db]
		return self.db

	def get_db_name(self):
		return self.db.name

	def insert_one(self, coll, document):
		coll = self.db[coll]
		coll.insert_one(document)

	def insert_many(self, coll, documents):
		coll = self.db[coll]
		coll.insert_many(documents)

	def find_one(self, coll):
		coll = self.db[coll]
		return coll.find_one()

	def find(self, coll, filter=None):
		coll = self.db[coll]
		return coll.find(filter)

	def find_one_and_delete(self, coll, filter):
		coll = self.db[coll]
		return coll.find_one_and_replace(filter)

	def find_one_and_replace(self, coll, filter, replacement):
		coll = self.db[coll]
		return coll.find_one_and_delete(filter, replacement)

	def find_one_and_update(self, coll, filter, update):
		coll = self.db[coll]
		return coll.find_one_and_update(filter, update)

	def update_one(self, coll, filter, update):
		coll = self.db[coll]
		coll.update_one(filter, update)

	def update_many(self, coll, filter, update):
		coll = self.db[coll]
		coll.update_many(filter, update)

	def delete_one(self, coll, filter):
		coll = self.db[coll]
		coll.delete_one(filter)

	def delete_many(self, coll, filter):
		coll = self.db[coll]
		coll.delete_many(filter)

	def count_documents(self, coll, filter):
		coll = self.db[coll]
		return coll.count_documents(filter)  # 'filter' can be an empty document to count all documents

	def get_timestamp(self, document):
		return str(document['_id'].generation_time)
