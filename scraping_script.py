import requests
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
import json


def get_urls(congress, year):
    """Computes the url path"""
    url = "https://www.govtrack.us/data/congress/"+str(congress)+"/votes/"+str(year)+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("a")
    titles = [title.text for title in titles]
    #Strip the root directory
    titles = titles[1:]
    return [url+title+"data.json" for title in titles]

def get_votes(congress, year, limit=0):
    """Given the congress number and year pickle each
    bill's roll call data in pandas dataframe format"""
    urls = get_urls(congress, year)
    #limit the size for debugging purposes
    if limit != 0 and limit < len(urls):
        urls = urls[:limit]

    for uri in urls:
        print(uri)
        #vreq = request(uri)
        #rollcall = json.loads(r.text)
        


