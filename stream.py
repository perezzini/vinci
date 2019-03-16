import pandas as pd
import utils.itertools as it

class DF():
    def __init__(self, path, usecols=None):
        self.chunks_gen = lambda: (chunk for chunk in pd.read_csv(path, usecols=usecols, chunksize=1))

    def iter_rows(self, predicate=lambda _: True):
        return lambda: (next(chunk.iterrows()) for chunk in self.chunks_gen() if predicate(chunk))

    def get_full_row(self, n, predicate=lambda _: True):
        rows = self.iter_rows(predicate=predicate)
        return it.nth(rows(), n)

    def get_rows_by_col_name(self, col_name, predicate=lambda _: True):
        rows = self.iter_rows(predicate=predicate)
        try:
            return lambda: (row[col_name] for index, row in rows())
        except Exception as e:
            print(e)
