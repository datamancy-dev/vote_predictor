import requests
import pandas as pd
import pickle
import requests
import json
import debug as db
import resource_paths as rp


def vote_request(congress, year, limit=0, request_timer=0):
    """Builds two roll call matrices for the passage
    votes of the house and senate on the specified congress
    and year."""

    house_urls, senate_urls = rp.get_vote_urls(congress, year)

    if db.none_check(house_urls, congress, year)\
        or db.none_check(senate_urls, congress, year):
        return

    build_n_pack(house_urls, congress, year, limit, request_timer, "h")
    build_n_pack(senate_urls, congress, year, limit, request_timer, "s")


def build_n_pack(urls, congress, year, limit=0, request_timer=0, fn=""):
    if limit > 0 and limit < len(urls):
        urls = urls[:limit]
    # setup rp.get_urls to return two url lists for house and senate
    iddf = build_iddf(urls[0])

    if db.none_check(iddf, congress, year):
        return

    vote_df = create_vote_df(urls, congress, year, request_timer)
    vote_df = iddf.merge(vote_df, left_index=True, right_index=True)
    h_filepath = rp.get_pickle_fp(congress, year, fn)
    rp.create_bill_list(vote_df, fn, congress, year)
    vote_df.to_pickle(h_filepath)


def create_bill_list(vote_df, fn, congress, year):
    """Pickles a bill list to be used by the bill scraper"""
    cols = vote_df.columns
    cols = cols[3:]
    name = rp.get_bill_list(congress, year, fn)
    with open(name, "wb") as f:
        pickle.dump(cols, f)


def create_vote_df(urls, congress, year, request_timer=0):
    """Creates vote matrix columns given the url"""
    column_list=[]
    for column in get_votes(urls):
        if column is None:
            continue
        if request_timer > 0:
            rp.time.sleep(request_timer)
        column_list.append(column)

    return pd.concat(column_list, axis=1)


def build_iddf(url):
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


def j_to_vseries(js, query=None):
    """Turns a json roll call page into a Pandas series"""
    vote_casted = {}
    if "votes" not in js:
        return None
    if query is None:
        if not right_votetype(js):
            return None

    for votetype in js["votes"]:
        for vote in js["votes"][votetype]:
            if type(vote) != dict: continue
            vote_casted[vote["id"]] = votetype_to_num(votetype) if not query else vote[query]
    name = js["bill"]["type"]+str(js["bill"]["number"]) if not query else query
    return pd.Series(vote_casted, name=name)


def right_votetype(js):
    """Determines a vote is a passage vote or not"""
    if "bill" in js and js["category"] == "passage" and "amendment" not in js:
        return True
    else:
        return False


def votetype_to_num(votetype):
    """Transform all yeas into ones and everything else to 0"""
    if votetype[0] == 'Y' or votetype[0] == 'y' or votetype[0] == 'A' or votetype[0] == 'a':
        return 1
    else:
        return 0

