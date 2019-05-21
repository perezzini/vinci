import pandas as pd
from utils import datasets
from nlp import retrieval
from sklearn.utils import shuffle

def v_exp_split(dataframe,
            test_size,
            data_labels,
            targets_label,
            full_corpus,
            text_rep_model,
            dict,
            sim_index,
            exp_num,
            preproc,
            print_info=True):
    # Split entire dataframe in training and validation sets
    df_train, df_test = datasets.split(dataframe,
                                    data_labels,
                                    targets_label,
                                    test_size,
                                    stratify=True)

    num_train_rel = len(df_train[df_train['type'] == 1])
    num_train_nrel = len(df_train[df_train['type'] == 0])

    # Expand only relevant observations from training set
    df_train_r_exp = retrieval.expand_dataset_with_sim_docs(df_train[df_train[targets_label] == 1][data_labels],
                                                            full_corpus,
                                                            sim_index,
                                                            exp_num,
                                                            text_rep_model,
                                                            dict,
                                                            preproc,
                                                            'text',
                                                            drop_duplicates=True)
    df_train_r_exp[targets_label] = 1

    # Expand only non relevant observations from training set
    df_train_nr_exp = retrieval.expand_dataset_with_sim_docs(df_train[df_train[targets_label] == 0][data_labels],
                                                            full_corpus,
                                                            sim_index,
                                                            exp_num,
                                                            text_rep_model,
                                                            dict,
                                                            preproc,
                                                            'text',
                                                            drop_duplicates=True)
    df_train_nr_exp[targets_label] = 0

    # Concatenate relevant and non relevant observations in final training set
    df_train = pd.concat([df_train_r_exp, df_train_nr_exp])
    len_df_train = len(df_train)

    # Delete all duplicates observations from training set: there
    # could be equal observations with different targets
    df_train.drop_duplicates(subset=['text'], keep='first', inplace=True)
    len_df_train_dups_out = len(df_train)

    # Verify and correct the case where test and training set are not disjoint
    intersected_df = pd.merge(df_test, df_train, how='inner', on=['text'])
    num_overlapped_test_train = len(intersected_df)
    if num_overlapped_test_train >= 1:
        # Drop rows from the training set
        obs = [t for t in intersected_df['text']]
        df_train = df_train[df_train['text'].map(lambda t: t not in obs)]

    if print_info:
        print('[Test set] Num of relevant observations:', len(df_test[df_test['type'] == 1]))
        print('[Test set] Num of non relevant observations:', len(df_test[df_test['type'] == 0]))
        print('\n')
        print('[Train set] Num of relevant observations:', num_train_rel)
        print('[Train set] Num of non relevant observations:', num_train_nrel)
        print('\n')
        print('[Expanded train set] Num of relevant observations:', len(df_train_r_exp))
        print('[Expanded train set] Num of non relevant observations:', len(df_train_nr_exp))
        print('\n')
        print('[Expanded (non duplicates) train set] Num of relevant observations:', len(df_train[df_train['type'] == 1]))
        print('[Expanded (non duplicates) train set] Num of non relevant observations:', len(df_train[df_train['type'] == 0]))
        print('[Expanded (non duplicates) train set] Total num of observations', len(df_train))
        print('\n')
        print('Number of overlapped observations between test and expanded train set =', num_overlapped_test_train)

    return shuffle(df_test), shuffle(df_train)
