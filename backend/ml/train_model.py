"""
train_model.py
Milestone 1: Data Prep & Training Script for Movie Vector Matcher

What this script does:
1. Reads the IMDb datasets title.basics.tsv.gz and title.ratings.tsv.gz
2. Filters movies only (titleType == 'movie'), drops noisy/incomplete rows
3. Builds features: normalized genre vectors (multi-hot), year, runtime, rating
4. Trains KMeans(n_clusters=6)
5. Saves:
   - model.pkl              -> KMeans model + StandardScaler + genre list (all in one dict)
   - movies_cleaned.parquet -> cleaned dataset with features and a cluster column

Usage:
    python train_model.py --basics title.basics.tsv.gz --ratings title.ratings.tsv.gz

Data can be downloaded here: https://datasets.imdbws.com/
"""

import argparse
import sys

import numpy as np
import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer

N_CLUSTERS = 6
MIN_VOTES = 1000  # filter out movies with very few votes (noise)
MIN_YEAR = 1950


def load_data(basics_path: str, ratings_path: str) -> pd.DataFrame:
    print("Loading title.basics ...")
    basics = pd.read_csv(
        basics_path,
        sep="\t",
        na_values="\\N",
        dtype={"startYear": "object", "runtimeMinutes": "object"},
        low_memory=False,
    )

    print("Loading title.ratings ...")
    ratings = pd.read_csv(ratings_path, sep="\t", na_values="\\N", low_memory=False)

    print("Merging tables ...")
    df = basics.merge(ratings, on="tconst", how="inner")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["titleType"] == "movie"].copy()

    df["startYear"] = pd.to_numeric(df["startYear"], errors="coerce")
    df["runtimeMinutes"] = pd.to_numeric(df["runtimeMinutes"], errors="coerce")
    df["averageRating"] = pd.to_numeric(df["averageRating"], errors="coerce")
    df["numVotes"] = pd.to_numeric(df["numVotes"], errors="coerce")

    df = df.dropna(subset=["startYear", "runtimeMinutes", "averageRating", "genres"])
    df = df[df["genres"] != "\\N"]

    df = df[
        (df["numVotes"] >= MIN_VOTES)
        & (df["startYear"] >= MIN_YEAR)
        & (df["runtimeMinutes"] >= 40)
        & (df["runtimeMinutes"] <= 240)
    ]

    df["genres_list"] = df["genres"].str.split(",")

    df = df.reset_index(drop=True)
    return df


def build_features(df: pd.DataFrame):
    # Genres -> multi-hot vector
    mlb = MultiLabelBinarizer()
    genre_matrix = mlb.fit_transform(df["genres_list"])
    genre_cols = [f"genre_{g}" for g in mlb.classes_]
    genre_df = pd.DataFrame(genre_matrix, columns=genre_cols, index=df.index)

    numeric_cols = ["startYear", "runtimeMinutes", "averageRating"]
    scaler = StandardScaler()
    numeric_scaled = scaler.fit_transform(df[numeric_cols])
    numeric_scaled_df = pd.DataFrame(
        numeric_scaled, columns=[f"{c}_scaled" for c in numeric_cols], index=df.index
    )

    features = pd.concat([genre_df, numeric_scaled_df], axis=1)
    return features, mlb, scaler, genre_cols, numeric_cols


def train_kmeans(features: pd.DataFrame) -> KMeans:
    print(f"Training KMeans(n_clusters={N_CLUSTERS}) ...")
    model = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    model.fit(features.values)
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--basics", default="title.basics.tsv.gz")
    parser.add_argument("--ratings", default="title.ratings.tsv.gz")
    parser.add_argument("--out_model", default="model.pkl")
    parser.add_argument("--out_data", default="movies_cleaned.parquet")
    args = parser.parse_args()

    try:
        df = load_data(args.basics, args.ratings)
    except FileNotFoundError as e:
        print(f"Error: dataset file not found -> {e}")
        sys.exit(1)

    print(f"Rows before cleaning: {len(df)}")
    df = clean_data(df)
    print(f"Rows after cleaning: {len(df)}")

    features, mlb, scaler, genre_cols, numeric_cols = build_features(df)
    model = train_kmeans(features)

    df["cluster"] = model.labels_
    # Keep the feature vectors too (needed for cosine_similarity on the backend)
    df = pd.concat([df.reset_index(drop=True), features.reset_index(drop=True)], axis=1)

    keep_cols = [
        "tconst",
        "primaryTitle",
        "startYear",
        "runtimeMinutes",
        "genres",
        "averageRating",
        "numVotes",
        "cluster",
    ] + list(features.columns)

    df_out = df[keep_cols]
    df_out.to_parquet(args.out_data, index=False)
    print(f"Saved cleaned dataset -> {args.out_data}")

    artifact = {
        "kmeans_model": model,
        "scaler": scaler,
        "mlb": mlb,
        "genre_cols": genre_cols,
        "numeric_cols": numeric_cols,
        "n_clusters": N_CLUSTERS,
    }
    joblib.dump(artifact, args.out_model)
    print(f"Saved model -> {args.out_model}")

    print("\nMovie count per cluster:")
    print(df_out["cluster"].value_counts().sort_index())


if __name__ == "__main__":
    main()
