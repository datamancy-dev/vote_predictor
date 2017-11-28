import pickle
from sys import argv
import pandas as pd
from sklearn.linear_model import LogisticRegression as lr
from sklearn.model_selection import cross_val_score as cvalscore

NAME, DFLIST = argv

def main(dffp):
    dflist = load_resource(dffp)
    mean_scores = trainlogreg_n_score(dflist)

    pack_resource("./"+dffp[2]+"_meanscores.pkl", mean_scores)

def trainlogreg_n_score(dflist):
    """Given a list of models train the passed in list of models with the given
    model type"""
    model_mean_scores = []

    for df in dflist:
        y = df.response.values
        feature_cols = [i for i in list(df.columns) if i != "response"]
        X = df.loc[:, feature_cols].as_matrix()

        logreg = lr(random_state=42, max_iter = 500)
        try:
            scores = cvalscore(logreg, X, y, cv=5, n_jobs=-1)
        except:
            pass
        model_mean_scores.append(scores.mean())

    return model_mean_scores

def load_resource(fp):
    with open(fp, "rb") as f:
        resource = pickle.load(f)

    return resource

def pack_resource(fp, resource):
    with open(fp, "wb") as f:
        pickle.dump(resource, f)

if __name__ == "__main__":
    main(DFLIST)
