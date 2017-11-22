import pickle
from sys import argv
import pandas as pd
import resource_path as rp

NAME, LAWM_PATH, VOTE_RESOURCE, CHAMBER = argv

def make_lawmakers_df(lawm_path, vote_resource, chamber):
    """Make the lawmaker model"""
    votes_p_congress = load_resource(vote_resource)
    response_cols = build_response_cols(votes_p_congress, lawm_path)

    dataframes = build_variables(response_cols)
    series_response_cols = pd.Series(response_cols)

    pack_resource(dataframes, "./"+chamber+"_modeldfs.pkl")
    pack_resource(series_response_cols, "./"+chamber+"_responsecols.pkl")


def pack_resource(resource, filepath):
    """Pickles given resource in filepath"""
    with open(filepath, "wb") as f:
        pickle.dump(resource, filepath)

#NOTE remember to add years and house column should you need them
def build_variables(response_cols):
    """Given list of dictionaries build a dataframe per dictionary that
    contains only the laws specified by the dictionary keys. Returns a list of
    dataframes of length equals to the number of lawmakers"""
    allbills = load_resource("./topictrimmedbills.pkl")
    all_vars = []
    for col in response_cols:
        lawmaker_bills = allbills.loc[col.keys()]
        del lawmaker_bills["years"]
        del lawmaker_bills["house"]

        all_vars.append(lawmaker_bills)

    return all_vars


def build_response_cols(votes_p_congress, lawm_path):
    """Builds all of the lawmakers response columns. Returns a list
    of dictionaries with length equal to the number of lawmakers."""
    lawm_dict = load_resource(lawm_path)
    response_cols = []
    congtoind = {109:2, 110:4, 111:3, 112:6, 113:5, 114:1, 115:0}

    for lawm, sessions in lawm_dict.items():
        response_col = {}
        for session in sessions:
            response_col = merge_dicts(response_col,
                    congress_response_col(votes_p_congress[congtoind[session]],
                        lawm))
        response_cols.append(response_col)

    return response_cols


def merge_dicts(dicta, dictb):
    """Combines the two dictionaries and returns the merged dict"""
    newdict = dicta.copy()
    newdict.update(y)

    return newdict

def congress_response_col(vote_df, lawm):
    """Given a vote dataframe and a lawmaker extract the votes from
       that lawmaker

       Returns a dictionary with bills in its keys and votes as its
       items"""

    congress_lawmaker_votes = vote_df.loc[lawm][:].to_dict()
    del congress_lawmaker_votes[vote_df.columns.values.tolist()[0]]

    return congress_lawmaker_votes


def load_resource(file_path):
    """Loads resource at given filepath"""
    with open(file_path, "rb") as f:
        resource =  pickle.load(f)

    return resource


if ___name__ == "__main__":
    make_lawmakers_df(LAWM_PATH, VOTE_RESOURCE, CHAMBER)
