"""Builds the corpus"""
import re
import pickle
import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


class StemTokenizer(object):
    def __init__(self):
        self.ps = PorterStemmer()
        self.reg = reg = re.compile(r'['+ string.punctuation + r'0-9]+')

    def __call__(self, doc):
        words = word_tokenize(doc)
        words = [word for word in words if self.reg.search(word) is None]

        return [self.ps.stem(word) for word in words]

# Save this df for using during feature engineering
def one_df():
    pass

def pre_merge(df, year):
    pass

def load_dir():
    pass

def preprocess():
    pass

def feature_engineer():
    pass

def penalized_l2_log_reg():
    pass

def prune():
    pass
