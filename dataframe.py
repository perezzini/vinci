class DataFrame():
    def __init__(self, pandas_df):
        self.df = pandas_df

    # Makes object subscriptable
    def __getitem__(self, item):
        return self.df[item]

    def head(self):
        return self.df.head()

    def info(self):
        self.df.info()

    def shape(self):
        return self.df.shape

    def list_series(self):
        return list(self.df.columns.values)

    def empty_it(self):
        self.df = pd.DataFrame()

    def replace(self, series, elem1, elem2):
        self.df[series].replace(elem1, elem2, inplace=True)

    def dropna(self, subset):
        self.df.dropna(subset=subset, inplace=True)

    def apply_to_series(self, func, series):
        self.df[series] = self.df[series].apply(func)

    def to_csv(self, path):
        self.df.to_csv(path)
