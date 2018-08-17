# BasicCrawler
State-of-the-art crawler using Python's scrapy and splash to crawl static/dynamic web pages.

# Installation
You need the following tools:
- Virtual env: pipenv
- Packages: scrapy, scrapy-splash, beautifulsoup4
- Docker: splash image to run a server

# Current spiders
- bo_nacional: crawl all norms from boletinoficial.gob.ar
- quotes: crawl all quotes from quotes.toscrape.com/js

They all return data objects in JL or JSON format using scrapy instructions.

# Deploy spiders
To deploy certain spider from the *crawler* project, do (inside pipenv shell):
1- Start scrapyd server executing ``scrapyd`` (always)
2- ``scrapyd-deploy`` (first-time only to generate some project files)
3- Finally, schedule some spider