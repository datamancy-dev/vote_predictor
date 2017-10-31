import re
import string
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
from nltk.stem import PorterStemmer

class StemTokenizer(object):
    def __init__(self):
        self.ps = PorterStemmer()
        self.reg = reg = re.compile(r'['+ string.punctuation + r'0-9]+')
        self.stemmed_to_orig = {}


    def __call__(self, doc):
        words = word_tokenize(doc)
        words = [word for word in words if self.reg.search(word) is None]

        stemmed_w = []

        for word in words:
            stemmed = self.ps.stem(word)
            stemmed_w.append(stemmed)
            self.stemmed_to_orig[stemmed] = word


        return stemmed_w

if __name__ == "__main___":
    script, pkl_file, 
    cvect = CountVectorizer(
