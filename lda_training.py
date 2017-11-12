"""Trains an LDA model and pickles it
arguments:
    - NUM_TOPICS: number of topics
    - DT_MAT: path to document term matrix
    - MODEL_NAME: the name of the model
    - MAX_ITER: maximum number of iterations"""

import pickle
from sys import argv
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import CountVectorizer

NAME, NUM_TOPICS, MAX_ITER, DT_MAT, MODEL_NAME = argv

def train_n_dump(name_dtmat, name_model, num_topics, m_iter):
    """Main function"""

    with open(name_dtmat, "rb") as f:
        dtmat = pickle.load(f)

    mlda = LDA(n_components=num_topics, learning_method='online',
            max_iter=m_iter, evaluate_every=4, total_samples=1663, n_jobs=-1,
            verbose=1, random_state=123)

    transformed = mlda.fit_transform(dtmat)

    with open("./"+name_model+".pkl", "wb") as f:
        pickle.dump(mlda, f)

    with open("./"+name_model+"_out.pkl", "wb") as f:
        pickle.dump(transformed, f)


if __name__ == '__main__':
    train_n_dump(DT_MAT, MODEL_NAME, int(NUM_TOPICS), int(MAX_ITER))

