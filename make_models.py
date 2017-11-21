import pickle
from sys import argv
import pandas as pd
import resource_path as rp

def make_lawmakers_df(lawm_path, vote_resource, chamber):
    """Make the lawmaker model"""
    lawm = load_resource(lawm_path)
    lawmaker_model_list = []

    votes_p_congress = load_resource(vote_resource)
    response_cols = build_response_cols(votes_p_congress)

    dataframes = build_variables(response_cols)

    series_response_cols = to_series(response_cols)

    pack_resource(dataframes, "./"+chamber+"_modeldfs.pkl")
    pack_resource(series_response_cols, "./"+chamber+"_responsecols.pkl")


def pack_resource(resource, filepath):
    """Pickles given resource in filepath"""
    with open(filepath, "wb") as f:
        pickle.dump(resource, filepath)

def to_series(response_cols):
    """Given a list of dictionaries return a list of series containing the same
    elements as the dictionaries"""


def build_variables(response_cols):
    """Given list of dictionaries build a dataframe per dictionary that
    contains only the laws specified by the dictionary keys. Returns a list of
    dataframes of length equals to the number of lawmakers"""


def build_response_cols(votes_p_congress):
    """Builds all of the lawmakers response columns"""
    response_col = {}
    congtoind = {109:2, 110:4, 111:3, 112:6, 113:5, 114:1, 115:0}

    for lawm, sessions in lawm_dict.items():
        for session in sessions:
            response_col = merge_dicts(response_col,
                    congress_response_col(votes_p_congress[congtoind[session]],
                        lawm))

    return response_col


def congress_response_col(vote_df, lawm):
    """Given a vote dataframe and a lawmaker extract the votes from
       that lawmaker

       Returns a dictionary with bills in its keys and votes as its
       items"""







def load_resource(file_path):
    """Loads resource at given filepath"""
    with open(file_path, "rb") as f:
        resource =  pickle.load(f)

    return resource


