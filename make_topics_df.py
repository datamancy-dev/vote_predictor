"""This file creates a topic dataframe given an LDA model"""
import pickle
import re
from sys import argv
from sklearn.decomposition import LatentDirichletAllocation as LDA
import pandas as pd

NAME, ALL_BILLS, LDA_MODEL, OUT_NAME = argv

def create_topics_df(bills, lda_out, out_name):
    with open(bills, "rb") as f:
        bills = pickle.load(f)

    with open(lda_out, "rb") as f:
        lda_out = pickle.load(f)

    topic_names = ["Topic-" + str(X) for X in xrange(lda_out.shape[1])]
    topic_df = pd.DataFrame(lda_out, index=bills.index, columns = topic_names)
    years, house = extract_y_and_house(topic_df.index.values.tolist())

    topic_df["years"] = years
    topic_df["house"] = house

    with open("./"+out_name, "wb") as f:
        pickle.dump(topic_df, f)


def extract_y_and_house(inds):
    years = []
    house = []
    for ind in inds:
        years.append(int(inds[:4]))
        house.append(inds[4])

    return years, house

if __name__ == '__main__':
    create_topics_df(ALL_BILLS, LDA_MODEL, OUT_NAME)
