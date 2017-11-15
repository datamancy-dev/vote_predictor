"""This file creates a topic dataframe given an LDA model"""
import pickle
import re
from sys import argv
from sklearn.decomposition import LatentDirichletAllocation as LDA
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

NAME, NUM_TOPICS, LDA_MODEL = argv

#Just placeholder so that cvect can exist
class StemTokenizer(object):
    def __init__():
        pass





def extract_y_and_house(inds):
    years = []
    house = []
    for ind in inds:
        years.append(int(inds[:4]))
        house.append(inds[4])

    return years, house

if __name__ == '__main__':
    y_and_h = extract_y_and_house()
    
