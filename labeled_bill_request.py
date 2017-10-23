import resource_paths as rp
import debug as db
import time
import json
import requests
import pickle
import pandas as pd
import resource_paths as rp


def lbl_list_request(congress, year, request_timer):
    pickle_df(congress, year, "h", request_timer)
    pickle_df(congress, year, "s", request_timer)


def pickle_df(congress, year, chamber, request_timer=0):
    """Builds a data frame whose index are bill codes, it has
        5 columns:
          - json_uri     : The URI for the bill's JSON file
          - txt_uri      : The URI for the bill's txt file
          - main_subject : The bill's main subject
          - subjects     : All of the subjects the bill is about
          - text         : The raw text of the bill
    """
    c_list = load_list(congress, year, chamber)

    df, js, txt = build_base_df(c_list, congress, year)

    subj_df = build_col_from_resource(c_list, js, "subjects_top_term", request_timer)
    df.merge(subj_df, left_index=True, right_index=True)

    text_col = build_col_from_resource(clist, txt, "text", request_timer, txt=True)
    df[text_col.name] = text_col

    df.to_pickle(get_bill_pickle_fp(congress, year, chamber))


def load_list(congress, year, typ):
    with open(rp.get_bill_list(congress, year, typ), "rb") as f:
            bill_list = pickle.load(f)

    return bill_list.columns.values.tolist()

def build_base_df(c_list, congress, year):
    """builds the first column of the dataframe"""

    js_resource, txt_resource = rp.get_bill_urls(congress, c_list)

    first = pd.Series(dict(zip(c_list, js_resource)), name="json_uri")
    second = pd.Series(dict(zip(c_list, txt_resource)), name="txt_uri")

    return pd.concat([first, second], axis=1), js_resource, txt_resource

def build_col_from_resource(index, resource_list, name, request_timer =0, txt=False):
    data = []
    data2 = []
    for resource in resource_list:
        datum = requests.get(resource)
        if not db.good_request(datum):
            data.append(None)
        if txt:
            data.append(datum.text)
            continue
        d1, d2 = json_query(datum.text)
        data.append(d1)
        data2.append(d2)
        if request_timer > 0:
            time.sleep(request_timer)
    if txt:
        return pd.Series(dict(zip(index, data)), name=name)
    else:
        s1 = pd.Series(dict(zip(index, data)), name="subjects_top_term")
        s2 = pd.Series(dict(zip(index, data2)), name="subjects")

        return pd.concat([s1, s2], axis=1)

def json_query(r):
    js = json.loads(r)
    if "subjects" in js and "subjects_top_term" in js:
        return  js["subjects_top_term"], js["subjects"]
