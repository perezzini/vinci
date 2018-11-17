import itertools
import unidecode
import re
import pandas as pd

def split_list_by_sep(l, sep):
	# TODO: re-implement this
	return [list(x[1]) for x in itertools.groupby(l, lambda x: x.startswith(sep)) if not x[0]]

def to_ascii(txt):
	return unidecode.unidecode(txt)

def has_numbers(string):
	return bool(re.search(r'\d', string))

def gen_all_dates(start, end):
    dates = pd.date_range(start=start, end=end)
    return (d for d in dates.strftime("%Y-%m-%d"))
