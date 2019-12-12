# vinci: *Legal Requirements Engineering*
Computer Science practice thesis development

## Important software used
- Docker
- Splash package: a Javascript rendering service. Used to render dynamic websites.
- MongoDB
- Pipvenv

## Crawler
Implemented some spiders to crawl certain websites containing legal documents from the Argentinian Gov. Must be runned under some time-based job scheduler like Cron.

## Local environment
Set the following paths in a .env file:

```
# Home
PROJECT_PATH=

# Database
DB_SERVER=
DB_PORT=
DB_NAME=

# Spanish language data
ES_PATH=${PROJECT_PATH}/data/spanish
ES_VOC_PATH=${ES_PATH}/voc.csv
ES_LEMMAS_PATH=${ES_PATH}/lemmas.txt
ES_STOPWORDS_PATH=${ES_PATH}/stopwords.csv
CONTEXT_STOPWORDS_PATH=${ES_PATH}/context-stopwords.csv


# SAIJ thesaurus
THESAURUS_PATH=${PROJECT_PATH}/data/thesaurus/saij/derecho-argentino.rdf

# Internet resources
BO_NACIONAL=https://www.boletinoficial.gob.ar/seccion/primera
BO_PROVINCIAL=https://www.santafe.gob.ar/boletinoficial
BO_MUNICIPAL=http://sanlorenzo.gob.ar/ordenanzas

```

## Install project's requirements
```
pipenv install
```

Python version 3.5.6

## Classifiers
Download 4 text classifiers (Derecho Ambiental -> Desechos peligrosos and Derecho Laboral -> Accidentes de trabajo) from this 
[link](https://www.dropbox.com/s/4c15ogj55v0xvit/text-classifiers.zip?dl=0).

- Note: refer to `test` folder for further instructions.
