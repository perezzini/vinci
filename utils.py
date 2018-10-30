import itertools
import unidecode
import re

def split_list_by_sep(l, sep):
	if sep in l:
		return [list(x[1]) for x in itertools.groupby(l, lambda x: x == sep) if not x[0]]
	else:
		raise Exception('[utils] split_list_by_sep(): sep not in list')  # TODO: create better exceptions

def to_ascii(txt):
	return unidecode.unidecode(txt)

def has_numbers(string):
	return bool(re.search(r'\d', string))
