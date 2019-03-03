import itertools
import unidecode
import pandas as pd
import urllib.parse

def split_list_by_sep(l, sep):
	# TODO: re-implement this
	return [list(x[1]) for x in itertools.groupby(l, lambda x: x.startswith(sep)) if not x[0]]

def to_ascii(txt):
	return unidecode.unidecode(txt)

def gen_all_dates(start, end):
    dates = pd.date_range(start=start, end=end)
    return (d for d in dates.strftime("%Y-%m-%d"))

def iri_to_uri(iri):
	uri = urllib.parse.urlsplit(iri)
	uri = list(uri)
	uri[2] = urllib.parse.quote(uri[2])
	uri = urllib.parse.urlunsplit(uri)
	return uri
