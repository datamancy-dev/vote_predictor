import requests
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
import json

def get_votes(congress, year, limit=0):
    """Given the congress number and year yield a pandas series to be 
    aggregated in a pandas df"""

    urls = get_urls(congress, year)
    #limit the size for debugging purposes
    if limit > 0 and limit < len(urls):
        urls = urls[:limit]

    for uri in urls:
        print(uri)
        vreq = request(uri)
        yield j_to_vseries(json.loads(r.text))

def get_urls(congress, year):
    """Computes the url paths for the given congress and year"""
    url = "https://www.govtrack.us/data/congress/"+str(congress)+"/votes/"+str(year)+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("a")
    titles = [title.text for title in titles]
    #Strip the root directory
    titles = titles[1:]
    return [url+title+"data.json" for title in titles]


def j_to_vseries(js):
    """Turns a json roll call page into a Pandas series"""
    dic = {}
    for votetype in js["votes"]:
        for vote in js["votes"][votetype]:
            dic[vote["id"]] = votetype
    
    return pd.Series(dic, name=js["vote_id"])
