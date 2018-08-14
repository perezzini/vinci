import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Retrieve database config
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")