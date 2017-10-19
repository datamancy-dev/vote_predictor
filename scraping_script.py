import requests
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
import json

def get_votes(congress, year, limit=0):
    """Given the congress number and year pickle each
    bill's roll call data in pandas dataframe format"""

    url = "https://www.govtrack.us/data/congress/"+congress+"/votes/"+year+"/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("a")
    titles = [title.text for title in titles]
    #Strip the root directory
    titles = titles[1:]
    urls = [url+title+"/data.json" for title in titles]
    
    #I know it is inefficient to place this here but idk if I can
    #exit any of the of the for loops in list comprehensions early ASK or LU
    #limit the size for debugging purposes
    if limit != 0 and limit < len(urls):
        urls = urls[:limit]

    for uri in urls:
        vreq = request(uri)
        rollcall = json.loads(r.text)
