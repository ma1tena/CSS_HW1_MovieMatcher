"""
main.py
Milestone 2: FastAPI backend for Movie Vector Matcher.

Run locally (from the backend/ folder):
    uvicorn app.main:app --reload

Environment variables (optional):
    MODEL_PATH  - path to model.pkl (default: ml/model.pkl)
    DATA_PATH   - path to movies_cleaned.parquet (default: ml/movies_cleaned.parquet)
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .recommend import Recommender
from .schemas import QuizAnswers, RecommendResponse

app = FastAPI(title="Movie Vector Matcher API", version="1.0.0")

# CORS: open for now so the Vercel-hosted frontend can call this API
# during development. Restrict allow_origins to your deployed frontend
# URL once it's live (Milestone 5).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
