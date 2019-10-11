import pandas as pd
from sklearn.model_selection import train_test_split

def split(dataframe,
        data_labels,
        targets_label,
        test_size,
        stratify=False,
        random_state=None):
    if stratify:
        X_train, X_test, y_train, y_test = train_test_split(dataframe[data_labels],
                                                            dataframe[targets_label],
                                                            test_size=test_size,
                                                            random_state=random_state,
                                                            stratify=dataframe[targets_label])
    else:
        X_train, X_test, y_train, y_test = train_test_split(dataframe[data_labels],
                                                            dataframe[targets_label],
                                                            test_size=test_size,
                                                            random_state=random_state)
    df_train = pd.concat([pd.DataFrame(X_train), pd.DataFrame(y_train)], axis=1)
    df_test = pd.concat([pd.DataFrame(X_test), pd.DataFrame(y_test)], axis=1)

    return df_train, df_test

def load_and_sample(n,
                    file_path,
                    usecols=None):
    df = pd.read_csv(file_path, usecols=usecols)
    if n >= len(df):
        return df
    else:
        return df.sample(n=n)
