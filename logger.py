import logging

class Log():
	def __init__(self):
		logging.basicConfig(filename='.log',
							level=logging.DEBUG,
							format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

	def warning(self, msg):
		logging.warning(msg)


	def info(self, msg):
		logging.info(msg)

	def debug(self, msg):
		logging.debug(msg)