import requests
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
import json
import time
import debug as db


def build_n_pack(congress, year, limit=0, request_timer=0):
    """Build's a roll call matrix from the specified congress
    in a given year. The indeces of the columns correspond to the
    lawmaker's id. Other identifying information includes:
        Name
        Party
        State
    The rest of the columns are bills identified by "vote_id"
    each field is a 0 for nay or present, a 1 for aye """

    urls = get_urls(congress, year)
    if db.none_check(urls, congress, year):return
    urls = urls[:limit] if limit > 0 and limit < len(urls) else urls
    # setup get_urls to return two url lists for house and senate
    # separate the part bellow this to call the function twice
    # and pickle two objects per call.
    df = build_id_df(urls[0])
    if db.none_check(df, congress, year):return
    column_list=[]
    for column in get_votes(urls):
        if column is None:continue
        if request_timer > 0:time.sleep(request_timer)
        column_list.append(column)

    vote_df = pd.concat(column_list, axis=1)
    df = df.merge(vote_df, left_index=True, right_index=True)
    filepath = './votes-'+str(congress)+"-"+str(year)+".pkl"
    df.to_pickle(filepath)
    

def build_id_df(url):
    """Builds the identifying information DataFrame
    this function is horrible"""
    req = requests.get(url)
    if not db.good_request(req):
        return None

    js = json.loads(req.text)

    fields = ["display_name", "party", "state"]
    columns = [j_to_vseries(js, feature) for feature in fields]
    
    return pd.concat(columns, axis=1)

def get_votes(urls):
    """Given the congress number and year yield a pandas series to be
    aggregated in a pandas df.
    Many preemptive thanks to govtrack.us for not banning my ip
    for running this code. (hopefully)"""
    for url in urls:
        vreq = requests.get(url)
        if not db.good_request(vreq): continue
        yield j_to_vseries(json.loads(vreq.text))


def get_urls(congress, year):
    """Computes the url paths for the given congress and year."""
    url = "https://www.govtrack.us/data/congress/"+str(congress)+"/votes/"+str(year)+"/"
    r = requests.get(url)
    if not db.good_request(r):return None

    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("a")
    titles = [title.text for title in titles]
    #Strip the parent directory
    titles = titles[1:]
    return [url+title+"data.json" for title in titles]


def j_to_vseries(js, query=None):
    """Turns a json roll call page into a Pandas series"""
    vote_casted = {}
    if "votes" not in js:
        return None
    for votetype in js["votes"]:
        for vote in js["votes"][votetype]:
            vote_casted[vote["id"]] = votetype if not query else vote[query]
    name = js["vote_id"] if not query else query
    return pd.Series(vote_casted, name=name)
