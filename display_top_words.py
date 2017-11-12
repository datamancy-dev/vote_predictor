"""Displays the top terms in the given LDA model"""
from sys import argv
import pickle
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

NAME, N_TOP_WORDS, LDA_MODEL, CVECT = argv

def main(n_words, lda_model, cvect):
    """main"""
    vocab, model = load_vocab_and_model(cvect, lda_model)

    topic_words = make_topic_word_dict(vocab, model, n_words)

    print_topic_word_dict(topic_words)

def load_vocab_and_model(cvect, lda_model):
    """Self explanatory"""
    with open(cvect, "rb") as f:
        cvect = pickle.load(f)

    vocab = cvect.get_feature_names()

    with open(lda_model, "rb") as f:
        model = pickle.load(f)

    return vocab, model

def make_topic_word_dict(vocab, model, n_words):
    """Makes a maping of top terms per topic in an LDA model"""
    topic_words = {}
    for topic, comp in enumerate(model.components_):
        word_idx = np.argsort(comp)[::-1][:n_words]

        topic_words[topic] = [vocab[i] for i in word_idx]

    return topic_words

def print_topic_word_dict(topic_words):
    """Self explanatory"""
    for topic, words in topic_words.items():
        print('\n\nTopic: %d \n' % topic)
        print('%s' % '\n'.join(words))

#Placeholder so that cvect can exist
class StemTokenizer(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    main(int(N_TOP_WORDS), LDA_MODEL, CVECT)
