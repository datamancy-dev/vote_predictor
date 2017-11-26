import pickle
import re
from sys import argv
import pandas as pd

NAME, LAWM_PATH, VOTE_RESOURCE, CHAMBER = argv

def make_lawmakers_df(lawm_path, vote_resource, chamber):
    """Make the lawmaker model"""
    votes_p_congress = load_resource(vote_resource)
    response_cols = build_response_cols(votes_p_congress, lawm_path)

    dataframes = build_variables(response_cols)
    series_response_cols = [pd.Series(response_col) for response_col in
            response_cols]

    dataframes = [df for df in combinedflist(dataframes, series_response_cols)]

    pack_resource(dataframes, "./"+chamber+"_modeldfs.pkl")

def combinedflist(dataframes, response_cols):
    """combines a list of dataframes and response columns"""
    for i in xrange(len(dataframes)):
        dataframes[i]["response"] = response_cols[i]
        yield dataframes[i]

def pack_resource(resource, filepath):
    """Pickles given resource in filepath"""
    with open(filepath, "wb") as f:
        pickle.dump(resource, f)

#NOTE remember to add years and house column should you need them
def build_variables(response_cols):
    """Given list of dictionaries build a dataframe per dictionary that
    contains only the laws specified by the dictionary keys. Returns a list of
    dataframes of length equals to the number of lawmakers"""
    allbills = load_resource("./finaltopicsdf.pkl")
    all_vars = []
    for col in response_cols:
        lawmaker_bills = allbills.loc[col.keys()]

        lawmaker_bills.dropna(inplace=True)
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
    newdict.update(dictb)

    return newdict

def congress_response_col(vote_df, lawm):
    """Given a vote dataframe and a lawmaker extract the votes from
       that lawmaker

       Returns a dictionary with bills in its keys and votes as its
       items"""

    congress_lawmaker_votes = vote_df.loc[lawm][:].to_dict()

    congress_lawmaker_votes = del_pointone_col(congress_lawmaker_votes)

    del congress_lawmaker_votes[vote_df.columns.values.tolist()[0]]
    del congress_lawmaker_votes[vote_df.columns.values.tolist()[1]]
    del congress_lawmaker_votes[vote_df.columns.values.tolist()[2]]
    del congress_lawmaker_votes[vote_df.columns.values.tolist()[-1]]

    return congress_lawmaker_votes

def del_pointone_col(col):
    """Done to delete the bills that were voted on twice."""
    pointone = re.compile(r"\.1")
    list_to_del = [val for val in col.keys() if len(pointone.findall(val)) > 0]

    for val in list_to_del:
        del col[val]

    return col




def load_resource(file_path):
    """Loads resource at given filepath"""
    with open(file_path, "rb") as f:
        resource =  pickle.load(f)

    return resource


if __name__ == "__main__":
    make_lawmakers_df(LAWM_PATH, VOTE_RESOURCE, CHAMBER)
