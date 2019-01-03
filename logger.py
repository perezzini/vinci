import logging

class Log():
	def __init__(self):
		logging.basicConfig(filename='.log',
							level=logging.DEBUG,
							format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')
		# define a Handler which writes INFO messages or higher to the sys.stderr
		console = logging.StreamHandler()
		console.setLevel(logging.DEBUG)
		# set a format which is simpler for console use
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		# tell the handler to use this format
		console.setFormatter(formatter)
		# add the handler to the root logger
		logging.getLogger('').addHandler(console)

	def warning(self, msg):
		logging.warning(msg)


	def info(self, msg):
		logging.info(msg)

	def debug(self, msg):
		logging.debug(msg)
