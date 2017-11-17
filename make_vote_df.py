"""This file makes the vote dataframes as well as
the unique lawmakers dictionary """
import re
import pickle
from sys import argv
from collections import defaultdict
import subprocess as sp
import resource_paths as rp
import pandas as pd

NAME, CHAMBER=argv

def separate_by_congress(votefp):
    congresses = [str(num) for num in xrange(109,116)]
    links_list = defaultdict(list)

    for congress in congresses:
        congfind = re.compile(congress)
        for path in votefp:
            if congfind.search(path) is not None:
                links_list[congress].append(path)

    return links_list


def year_to_cong(year):
    ytc = {2005:109, 2006:109, 2008:110, 2009:111, 2010:111, 2011:112,
           2012:112, 2014:113, 2015:114, 2016:114, 2017:115}

    return ytc[year]



def create_congress_dflst(linkslist, house_initial):
    dfs = []
    for lst in linkslist:
        cur_cong_votes =[]
        years=[]
        for link in linkslist[lst]:
            with open(link, "rb") as f:
                df = pickle.load(f)
            df = reload_without_dupes(df,link)
            df, year= append_year(df, link, house_initial)
            cur_cong_votes.append(df)
            years.append(year)

        if len(cur_cong_votes) > 1:
            cur_cong_votes[1] = cur_cong_votes[1].iloc[:,4:]

        final_df = pd.concat(cur_cong_votes, axis=1)
        final_df["congress"]=year_to_cong(years[0])

        dfs.append(final_df)

    return dfs

def append_year(df, link, house_initial):
    find_year = re.compile(r"[0-9]{4}")
    year = find_year.search(link).group(0)
    new_name = year + house_initial + "-"
    df = df.add_prefix(new_name)

    return df, int(year)


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
            congress = int(df["congress"].iloc[0])
            unique_l[lawmaker].add(congress)


    return unique_l


if __name__ == '__main__':
    votefp = rp.get_all_dfs(CHAMBER+"vote")

    linkslist = separate_by_congress(votefp)

    dfs = create_congress_dflst(linkslist, CHAMBER)

    unique = unique_lawmakers(dfs)

    with open("./"+CHAMBER+"votes_p_congress.pkl", "wb") as f:
        pickle.dump(dfs, f)

    with open("./"+CHAMBER+"_lawmakers.pkl", "wb") as f:
        pickle.dump(unique, f)

