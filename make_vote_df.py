"""This file makes the vote dataframes as well as 
the unique lawmakers dictionary """
import re
import pickle
from sys import argv
from collections import defaultdict
import subprocess as sp
import resource_paths as rp
import pandas as pd

NAME, CHAMBER, OUTPUT=argv

def separate_by_congress(votefp):
    congresses = [str(num) for num in xrange(109,116)]
    links_list = defaultdict(list)

    for congress in congresses:
        congfind = re.compile(congress)
        for path in votefp:
            if congfind.search(path) is not None:
                links_list[congress].append(path)

    return links_list


def create_congress_dflst(linkslist, house_initial):
    dfs = []
    for lst in linkslist:
        cur_cong_votes =[]
        for link in linkslist[lst]:
            with open(link, "rb") as f:
                df = pickle.load(f)
            df = reload_without_dupes(df,link)
            df = append_year(df, link, house_initial)
            cur_cong_votes.append(df)
        if len(cur_cong_votes) > 1:
            cur_cong_votes[1] = cur_cong_votes[1].iloc[:,4:]
        dfs.append(pd.concat(cur_cong_votes, axis=1))

    return dfs

def append_year(df, link, house_initial):
    find_year = re.compile(r"[0-9]{4}")
    year = find_year.search(link).group(-1)
    new_name = year + house_initial + "-"
    df = df.add_prefix(new_name)
    #This is kinda yanky but the fastest solution I found
    df["year"] = int(year)

    return df


def reload_without_dupes(df, fp):
    """Pandas bundles duplicates in a dataframe...
       This behavior (and the existance of duplicates)
       was unexpected so to avoid scraping the data again.
       This is the workaround"""
    fp = fp[:-4] + ".csv"
    df.to_csv(fp, encoding='utf-8', sep=',')
    df = pd.read_csv(fp, encoding='utf-8', index_col=0, mangle_dupe_cols=True, sep=',')

    sp.call(["rm", fp])

    return df


def unique_lawmakers(votes):
    """Makes a set with all of the lawmakers' IDs"""
    unique_l = defaultdict(set)

    for df in votes:
        for lawmaker in df.index.values.tolist():
            unique_l[lawmaker].add(df["year"])
    return unique_l


if __name__ == '__main__':
    votefp = rp.get_all_dfs(CHAMBER+"vote")

    linkslist = separate_by_congress(votefp)

    dfs = create_congress_dflst(linkslist, CHAMBER)

    with open("./"+OUTPUT+".pkl", "wb") as f:
        pickle.dump(dfs, f)

