import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class HistoricalRetriever:

    def __init__(self, data_path="data/amazon_historical_pairs.csv"):
        self.df = pd.read_csv(data_path)

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english"
        )

        self.matrix = self.vectorizer.fit_transform(
            self.df["customer_text"].fillna("")
        )

    def search(self, query, top_k=3):
        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix
        ).flatten()

        top_indices = scores.argsort()[-top_k:][::-1]

        results = self.df.iloc[top_indices].copy()
        results["similarity"] = scores[top_indices]

        return results[
            ["customer_text", "amazon_reply", "similarity"]
        ]