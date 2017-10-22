import requests
import debug as db
from bs4 import BeautifulSoup

def get_pickle_fp(congress, year, typ):
    return typ + "-" + str(congress)+"-"+str(year)+".pkl"

def get_bill_list(congress, year, typ):
    return typ + "-" + str(congress) + "-" + str(year)

def get_vote_urls(congress, year):
    """Computes the url paths for the given congress and year."""
    url = "https://www.govtrack.us/data/congress/"+str(congress)+"/votes/"+str(year)+"/"
    r = requests.get(url)
    if not db.good_request(r):return None

    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("a")
    titles = [title.text for title in titles]
    #Strip the parent directory
    titles = titles[1:]
    
    house_urls = [url+title+"data.json" for title in titles if title[0] == 'h']
    senate_urls = [url+title+"data.json" for title in titles if title[0] == 's']

    return house_urls, senate_urls
