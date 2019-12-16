# vinci: *Legal Requirements Engineering*
Computer science project thesis development.

**Abstract**: *Within legal engineering, artificial agents are needed with the ability to extract knowledge and patterns within legal documents to create applications that assist professionals to perform certain tasks, many of which need to be executed in real time, recovering and analyzing regulations of the official bulletins. Currently, the search for relevant regulations for certain activities within a company is done manually and involves numerous professionals from different areas within it. In the industrial field, the previous task is known as legal requirements engineering. This work proposes an online support system for legal engineering in order to transform legal requirements engineering into a semi-automatic activity.*

Luciano Perezzini, Universidad Nacional de Rosario

2018 - 2019

## Important software used
- Docker
- Splash package: a Javascript rendering service. Used to render dynamic websites.
- MongoDB
- Pipvenv

## Crawlers
Implemented multiple spiders to crawl websites containing legal documents from the Argentinian Gov. Must be runned under some time-based job scheduler like Cron.

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

Python version `3.5.6`

## Classifiers
Four text classifiers (*Derecho Ambiental -> Desechos peligrosos* and *Derecho Laboral -> Accidentes de trabajo*) were trained and are available from this [link](https://www.dropbox.com/s/4c15ogj55v0xvit/text-classifiers.zip?dl=0).

- Note: refer to `test` folder for further instructions.

---

> *"It had long since come to my attention that people of accomplishment rarely sat back and let things happen to them. They went out and happened to things."*
