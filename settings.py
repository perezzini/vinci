import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Retrieve database config
DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Lemmas
ES_LEMMAS_PATH = os.getenv('ES_LEMMAS_PATH')

# Legal terms vocabulary path
LEGAL_VOC_RDF_PATH = os.getenv('LEGAL_VOC_RDF_PATH')
LEGAL_VOC_API_PATH = os.getenv('LEGAL_VOC_API_PATH')
