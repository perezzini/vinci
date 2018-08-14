# Main module: where code must run

import logging
from database import DB

logging.basicConfig(filename='.log',
					level=logging.DEBUG,
					format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

print('Main started...')
print('----------------\n')

mongo_client = DB()

# Do some more work...

if __name__ == "__main__":
    logging.warning("I'm a warning!")   
    logging.info("Hello, Python!")
    logging.debug("I'm a debug message!")

mongo_client.close_conn()

print('\n----------------')
print('Main finished')