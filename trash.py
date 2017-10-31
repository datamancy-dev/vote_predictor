import re
import string 
from nltk import word_tokenize 
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import pickle

with open("./topictrimmedbills.pkl", "rb") as f:
     bills = pickle.load(f)


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

tokenz = StemTokenizer()

cvect = CountVectorizer(tokenizer=tokenz, stop_words="english",
        ngram_range=(2, 3), max_df=.8, min_df=30)

dt_mat = cvect.fit_transform(bills.text)

with open("./2n3ngramsdtmat.pkl", "wb") as f:
    pickle.dump(dt_mat, f)


