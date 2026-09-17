"""
main.py
Milestone 2: FastAPI backend for Movie Vector Matcher.

Run locally (from the backend/ folder):
    uvicorn app.main:app --reload

Environment variables (optional):
    MODEL_PATH   - path to model.pkl (default: ml/model.pkl)
    DATA_PATH    - path to movies_cleaned.parquet (default: ml/movies_cleaned.parquet)
    CORS_ORIGINS - comma-separated list of allowed frontend origins
                   (default: "*", i.e. allow everything — fine for local
                   dev, but set this to your Vercel URL in production,
                   see Milestone 5 / render.yaml)
"""

import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .recommend import Recommender
from .schemas import QuizAnswers, RecommendResponse

app = FastAPI(title="Movie Vector Matcher API", version="1.0.0")

# CORS_ORIGINS="*" (default) allows any origin — convenient for local
# development. In production (Render), set CORS_ORIGINS to a comma-separated
# list of allowed origins, e.g.:
#   CORS_ORIGINS=https://your-app.vercel.app,https://your-custom-domain.com
_raw_origins = os.getenv("CORS_ORIGINS", "*")
allowed_origins = ["*"] if _raw_origins == "*" else [o.strip() for o in _raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender: Optional[Recommender] = None


@app.on_event("startup")
def load_recommender() -> None:
    global recommender
    recommender = Recommender()


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Movie Vector Matcher API"}


@app.post("/api/recommend", response_model=RecommendResponse)
def recommend(answers: QuizAnswers):
    if recommender is None:
        raise HTTPException(status_code=503, detail="Model is not loaded yet")

    try:
        analytics, movies = recommender.recommend(answers)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"cluster": analytics, "movies": movies}

