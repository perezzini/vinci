from nlp import simtools
from nlp import doctools
import pandas as pd

def get_sim_docs_from_dataset(doc,
                            model,
                            dict,
                            preproc,
                            n,
                            sim_index,
                            dataset):
    """
    Retrieve the most n similar documents in a dataset, using cosine similarity.

    Parameters:
        - dataset must be a dictionary of texts
    """
    doc_bow = doctools.to_bow(doc, dict, preproc, model)
    sims = simtools.get_most_sim_doc_ids(doc_bow, n, sim_index)
    return [dataset[i] for i in sims]

def get_less_sim_docs_from_dataset(doc,
                                model,
                                dict,
                                preproc,
                                n,
                                sim_index,
                                dataset):
    """
    Retrieve the most n similar documents in a dataset, using cosine similarity.

    Parameters:
        - dataset must be a dictionary of texts
    """
    doc_bow = doctools.to_bow(doc, dict, preproc, model)
    sims = simtools.get_less_sim_doc_ids(doc_bow, n, sim_index)
    return [dataset[i] for i in sims]


def expand_dataset_with_sim_docs(dataset,
                                docs_coll,
                                sim_index,
                                n,
                                model,
                                dict,
                                preproc,
                                col_label,
                                drop_duplicates=True):
    """
    Expands each document in a given dataset with a set of the most similar documents
    from a collection of documents.

    Parameters:
        -   dataset: set of documents to expand
        -   docs_coll: set of documents used to expand input documents
        -   n: number of expansion per document
        -   model: vector space model representation of documents
        -   dict: dictionary of available terms
        -   preproc: preprocessing function to apply to each document in dataset
        -   del_duplicates: delete duplicates text in final expansion set
        -   col_label: label to use as column header in final expansion set
    """
    sim_docs = (get_sim_docs_from_dataset(doc,
                                        model,
                                        dict,
                                        preproc,
                                        n,
                                        sim_index,
                                        docs_coll) for doc in dataset)
    df = pd.DataFrame(columns=[col_label])
    for l in sim_docs:
        df = pd.concat([df, pd.DataFrame(data={col_label: l})])

    # Aggregate seeds
    df = pd.concat([df, pd.DataFrame(dataset)])  # FIXME: fix column names when concatenating

    if drop_duplicates:
        df.drop_duplicates(subset=[col_label], keep='first', inplace=True)

    return df.reset_index(drop=True)
