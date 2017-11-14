"""This file creates a topic dataframe given an LDA model"""
import pickle
import re
from sys import argv
from sklearn.decomposition import LatentDirichletAllocation as LDA
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

#Just placeholder so that cvect can exist
class StemTokenizer(object):
    def __init__():
        pass



