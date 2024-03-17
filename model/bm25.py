import os
import pandas as pd
import numpy as np
from nltk import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
from loguru import logger
import pickle
from .preprocessing import preprocess


class BM25(object):
    vectorizer: TfidfVectorizer

    def __init__(self, b=0.75, k1=1.6):
        self.vectorizer = TfidfVectorizer(
            norm=None,
            smooth_idf=False,
            ngram_range=(1, 3),
            preprocessor=self.preprocess,
        )
        self.b = b
        self.k1 = k1

    def fit(self, X):
        """Fit IDF to documents X"""
        self.vectorizer.fit(X)
        y = super(TfidfVectorizer, self.vectorizer).transform(X)
        self.X = y
        self.avdl = y.sum(1).mean()

    def transform(self, q):
        """Calculate BM25 between query q and documents X"""
        b, k1, avdl = self.b, self.k1, self.avdl

        len_X = self.X.sum(1).A1

        (q,) = super(TfidfVectorizer, self.vectorizer).transform([q])

        assert sparse.isspmatrix_csr(q)
        # convert to csc for better column slicing
        X = self.X.tocsc()[:, q.indices]
        denom = X + (k1 * (1 - b + b * len_X / avdl))[:, None]
        idf = self.vectorizer._tfidf.idf_[None, q.indices] - 1.0
        numer = X.multiply(np.broadcast_to(idf, X.shape)) * (k1 + 1)
        return (numer / denom).sum(1).A1

    def preprocess(self, s: str):
        ps = PorterStemmer()
        stopwords_set = set(stopwords.words("english"))
        stop_dict = {s: 1 for s in stopwords_set}
        return preprocess(ps, stop_dict, s)


def build_bm25_model():
    paths = [
        {
            "path": "data/bm25_recipe_name.pkl",
            "name": "cleaned_name",
        },
        {
            "path": "data/bm25_recipe_instruction.pkl",
            "name": "cleaned_instruction",
        },
        {
            "path": "data/bm25_recipe_ingredient.pkl",
            "name": "cleaned_ingredient",
        },
    ]

    df = pd.read_parquet("data/cleaned_recipes.parquet")
    for path in paths:
        if not os.path.exists(path["path"]):
            bm25 = BM25()
            bm25.fit(df[path["name"]])
            pickle.dump(bm25, open(path["path"], "wb"))
            logger.info(f"✅ BM25 model for {path['name']} is saved to {path['path']}")
        else:
            logger.info(f"✅ {path['path']} already exists")
