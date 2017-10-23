import requests
import debug as db
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime as dt


def get_bill_pickle_fp(congress, year, typ):
    return typ + "bill" +"-" + str(congress)+"-"+str(year)+".pkl"

def get_vote_pickle_fp(congress, year, typ):
    return typ + "vote" +"-" + str(congress)+"-"+str(year)+".pkl"

def get_bill_list(congress, year, typ):
    return typ + "-" + str(congress) + "-" + str(year)+".pkl"

def get_vote_urls(congress, year):
    """Computes the url paths for the given congress and year."""
    url = "https://www.govtrack.us/data/congress/"+str(congress)+"/votes/"+str(year)+"/"
    r = requests.get(url)
    if not db.good_request(r):return None
    titles = extract_dir_names(r)

    house_urls = [url+title+"data.json" for title in titles if title[0] == 'h']
    senate_urls = [url+title+"data.json" for title in titles if title[0] == 's']
    return house_urls, senate_urls

def get_bill_urls(congress, to_select):
    """Crawls the site getting the links to the files that matter
    Returns a list of the urls that matters"""

    root_dir = "https://www.govtrack.us/data/congress/"+ str(congress)+"/bills/"
    root = requests.get(root_dir)

    if not db.good_request(root):
        return None
    
    sub_roots = extract_dir_names(root)
    sub_roots = [root_dir + s_root for s_root in sub_roots]
    all_bills = []
    bill_titles = []
    for s_root in sub_roots:
        leaf = requests.get(s_root)
        if not db.good_request(leaf):
            return None
        bills = extract_dir_names(leaf)
        bill_titles += bills
        all_bills += [s_root+title for title in bills]

    # Keep in mind that these bill titles have a front-slash at the end
    bill_dic = dict(zip(bill_titles, all_bills))
    # Only pick the bills that got to the passage vote
    all_bills = [bill_dic[bill+"/"] for bill in to_select]

    json_paths = [bill + "data.json" for bill in all_bills]
    text_dirs = [bill + "text-versions/" for bill in all_bills]
    text_dirs = [bill + "document.txt" for bill in get_text_urls(text_dirs)]

    return json_paths, text_dirs


def get_text_urls(text_dirs):
    for url in text_dirs:
        text_dir = requests.get(url)
        dir_names = extract_dir_names(text_dir)
        dates, key = extract_dates(text_dir)
        datesdir = dict(zip(dates, dir_names))
        #time.sleep(2)
        yield url + datesdir[key]


def extract_dates(r):
    """Returns dates out of html and the most recent one"""
    soup = BeautifulSoup(r.text, "html.parser")
    pre = soup.find_all("pre")
    raw = pre.pop()

    date_pattern = re.compile(r'[0-9][0-9]-[a-z A-Z]+-[0-9]{4}')
    list_of_dates = date_pattern.findall(raw.text)
    list_of_dates = [date for date in num_date(list_of_dates)]

    most_recent = max_date(list_of_dates)

    return list_of_dates, most_recent

def num_date(dates):
    daypattern = re.compile(r'[0-9]{2}-')
    monthpattern = re.compile(r'[A-Za-z]+')
    yearpattern = re.compile(r'[0-9]{4}')

    monthtonum = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
                  'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                  'Nov': 11, 'Dec': 12}

    for date in dates:
        daypart = daypattern.findall(date)
        daypart = int(daypart[0][:-1])

        monthpart = monthpattern.findall(date)
        monthpart = monthtonum[monthpart[0]]

        yearpart = yearpattern.findall(date)[0]
        yearpart = yearpart[-2:]

        yield dt.strptime(str(monthpart)+"/"+str(daypart)+"/"+yearpart,
                          "%m/%d/%y")


def max_date(dates):
    md = dt.strptime('1/1/90', "%m/%d/%y")

    for date in dates:
        md = date if date > md else md

    return md

def extract_dir_names(r):
    soup = BeautifulSoup(r.text, "html.parser")
    titles = soup.select("a")
    titles = [title.text for title in titles]
    #Strip the parent directory
    titles = titles[1:]

    return titles
