from sys import argv
import pickle
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

name, n_top_words, lda_model, cvect = argv


#Placeholder so that cvect can exist
class StemTokenizer(object):
    def __init__(self):
        pass

with open(cvect, "rb") as f:
    cvect = pickle.load(f)

vocab = cvect.get_feature_names()

with open(lda_model, "rb") as f:
    model = pickle.load(f)


topic_words = {}

for topic, comp in enumerate(model.components_):
    word_idx = np.argsort(comp)[::-1][:n_top_words]

    topic_words[topic] = [vocab[i] for i in word_idx]

for topic, words in topic_words.items():
    print('Topic: %d' % topic)
    print('%s' % '\n'.join(words))

