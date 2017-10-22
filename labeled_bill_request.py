import resource_paths as rp
import debug as db
import time
import json
import requests
import pickle
import pandas as pd
import resource_paths as rp

def lbl_bill_request(congress, year, limit=0, request_timer=0):
    """Builds a data frame whose index are bill codes, it has
        3 columns:
          - main_subject : The bill's main subject
          - subjects     : All of the subjects the bill is about
          - text         : The raw text of the bill
    """
    #Get bill title dictionary from pickle file in directory
    #Build a column with bill titles and bill names as its values
    #Build a list of all of the links to the bills
    #Build a list with all of the titles to the bills
    #Zip em in a dictionary
    #use the bill title dictionary from the beginning to prune and
    #separate the bill list
    #make requests to those bills and pickle em up in two dictionaries

def load_list(congress, year, typ):
    with open(rp.get_bill_list(congress, year, typ), "rb") as f:
            bill_list = pickle.load(f)

    return bill_list.columns.values.tolist()

def build_base_df(congress, year):
    """builds the first column of the dataframe"""
    s_list = load_list(congress, year, "h")
    h_list = load_list(congress, year, "s")


