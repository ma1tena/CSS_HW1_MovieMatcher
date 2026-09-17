"""
recommend.py
Core ML-inference logic: builds a User Vector from quiz answers,
predicts the KMeans cluster, and finds the top-N nearest movies
inside that cluster via cosine similarity.
"""

import os
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = os.getenv("MODEL_PATH", "ml/model.pkl")
DATA_PATH = os.getenv("DATA_PATH", "ml/movies_cleaned.parquet")

# The 5 anchor movies offered in the quiz -> their IMDb tconst.
# NOTE: verify these tconst values exist in your movies_cleaned.parquet
# (they should, since all 5 are high-vote-count titles), and swap them
# if your MIN_VOTES / MIN_YEAR filtering in train_model.py excluded any.
ANCHOR_MOVIES = {
    "Interstellar": "tt0816692",
    "The Dark Knight": "tt0468569",
    "La La Land": "tt3783958",
    "John Wick": "tt2911666",
    "How to Lose a Guy in 10 Days": "tt0309530",
}

ERA_YEAR_MAP = {"before2000": 1990, "2000-2015": 2008, "2016+": 2021}
DURATION_MINUTES_MAP = {1: 85, 2: 100, 3: 115, 4: 135, 5: 155}

# Genres nudged by the mood slider (1-2 = serious/heavy, 4-5 = light/fun)
MOOD_GENRES = {
    "low": ["Drama", "Thriller", "Mystery"],
    "high": ["Comedy", "Family", "Romance"],
}
# Genres nudged by the action/dynamics slider (1-2 = slow, 4-5 = high action)
ACTION_GENRES = {
    "low": ["Drama", "Romance"],
    "high": ["Action", "Adventure", "Sci-Fi", "Thriller"],
}

GENRE_BOOST_WEIGHT = 0.6  # how strongly quiz sliders nudge the anchor's genre vector


class Recommender:
    """Loads model artifacts once and serves recommendations."""

    def __init__(self, model_path: str = MODEL_PATH, data_path: str = DATA_PATH):
        artifact = joblib.load(model_path)
        self.kmeans = artifact["kmeans_model"]
        self.scaler = artifact["scaler"]
        self.mlb = artifact["mlb"]
        self.genre_cols = artifact["genre_cols"]
        self.numeric_cols = artifact["numeric_cols"]

        self.df = pd.read_parquet(data_path)
        self.feature_cols = self.genre_cols + [f"{c}_scaled" for c in self.numeric_cols]
        self.feature_matrix = self.df[self.feature_cols].values

    def _anchor_row(self, anchor_title: str) -> pd.Series:
        tconst = ANCHOR_MOVIES.get(anchor_title)
        if tconst is None:
            raise ValueError(f"Unknown anchor movie: {anchor_title}")

        row = self.df[self.df["tconst"] == tconst]
        if row.empty:
            raise ValueError(
                f"Anchor movie '{anchor_title}' ({tconst}) not found in the cleaned dataset. "
                "Check MIN_VOTES / MIN_YEAR filters in train_model.py."
            )
        return row.iloc[0]

    def _boost_genre_vector(self, base_vector: np.ndarray, mood: int, action: int) -> np.ndarray:
        vector = base_vector.copy().astype(float)

        weight_mood = (mood - 3) / 2  # -1 .. 1
        weight_action = (action - 3) / 2  # -1 .. 1

        mood_genres = MOOD_GENRES["high"] if weight_mood > 0 else MOOD_GENRES["low"]
        action_genres = ACTION_GENRES["high"] if weight_action > 0 else ACTION_GENRES["low"]

        for genre in mood_genres:
            col = f"genre_{genre}"
            if col in self.genre_cols:
                idx = self.genre_cols.index(col)
                vector[idx] += GENRE_BOOST_WEIGHT * abs(weight_mood)

        for genre in action_genres:
            col = f"genre_{genre}"
            if col in self.genre_cols:
                idx = self.genre_cols.index(col)
                vector[idx] += GENRE_BOOST_WEIGHT * abs(weight_action)

        return vector

    def build_user_vector(self, answers) -> Tuple[np.ndarray, str]:
        anchor = self._anchor_row(answers.anchor_movie)

        base_genre_vector = anchor[self.genre_cols].values.astype(float)
        genre_vector = self._boost_genre_vector(base_genre_vector, answers.mood, answers.action)

        target_year = ERA_YEAR_MAP[answers.era]
        target_runtime = DURATION_MINUTES_MAP[answers.duration]
        target_rating = float(anchor["averageRating"])  # anchor's own rating as a quality proxy

        numeric_raw = np.array([[target_year, target_runtime, target_rating]])
        numeric_scaled = self.scaler.transform(numeric_raw)[0]

        user_vector = np.concatenate([genre_vector, numeric_scaled])
        return user_vector, anchor["tconst"]

    def recommend(self, answers, top_n: int = 5):
        user_vector, anchor_tconst = self.build_user_vector(answers)

        cluster_label = int(self.kmeans.predict(user_vector.reshape(1, -1))[0])

        cluster_df = self.df[self.df["cluster"] == cluster_label].copy()
        cluster_features = cluster_df[self.feature_cols].values

        similarities = cosine_similarity(user_vector.reshape(1, -1), cluster_features)[0]
        cluster_df["similarity"] = similarities
        cluster_df = cluster_df[cluster_df["tconst"] != anchor_tconst]

        top_movies = cluster_df.sort_values("similarity", ascending=False).head(top_n)

        movies = []
        for _, row in top_movies.iterrows():
            match_percent = round(max(0.0, float(row["similarity"])) * 100, 1)
            movies.append(
                {
                    "tconst": row["tconst"],
                    "title": row["primaryTitle"],
                    "year": int(row["startYear"]),
                    "runtime": int(row["runtimeMinutes"]),
                    "genres": row["genres"],
                    "rating": float(row["averageRating"]),
                    "match_percent": match_percent,
                }
            )

        analytics = self._cluster_analytics(cluster_label)
        return analytics, movies

    def _cluster_analytics(self, cluster_label: int) -> dict:
        subset = self.df[self.df["cluster"] == cluster_label]

        genre_sums = subset[self.genre_cols].sum().sort_values(ascending=False)
        top_genres = [c.replace("genre_", "") for c in genre_sums.head(3).index]
        cluster_name = " & ".join(top_genres[:2]) + " Cluster"

        era_distribution = {
            "before2000": round(float((subset["startYear"] < 2000).mean()) * 100, 1),
            "2000-2015": round(float(subset["startYear"].between(2000, 2015).mean()) * 100, 1),
            "2016+": round(float((subset["startYear"] >= 2016).mean()) * 100, 1),
        }

        return {
            "cluster_id": cluster_label,
            "cluster_name": cluster_name,
            "avg_rating": round(float(subset["averageRating"].mean()), 2),
            "top_genres": top_genres,
            "era_distribution": era_distribution,
        }
