import pickle
from sys import argv
import pandas as pd
import resource_path as rp

def make_lawmakers_df(lawm_dict, vote_resource):
    lawm = load_lawmakers(lawm_dict)
    congtoind = {109:2, 110:4, 111:3, 112:6, 113:5, 114:1, 115:0}

    votes_p_congress = load_resource(vote_resource)
    lawm_list = []

            


def build_response_col():
    """Given a lawmaker, return the response variable column
       for its model"""
    for lawm, sessions in lawm_dict.items():
        for session in sessions:
            #get lawmakers row and save it as a series


def load_resource(file_path):
    """Loads resource at given filepath"""
    with open(file_path, "rb") as f:
        resource =  pickle.load(f)

    return resource


