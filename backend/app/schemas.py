"""
schemas.py
Pydantic request/response models for the Movie Vector Matcher API.
"""

from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class QuizAnswers(BaseModel):
    """Raw answers coming from the frontend quiz (Milestone 3)."""

    mood: int = Field(..., ge=1, le=5, description="1 = calm/serious, 5 = fun/light")
    action: int = Field(..., ge=1, le=5, description="1 = slow-paced, 5 = high action/dynamics")
    duration: int = Field(..., ge=1, le=5, description="1 = short movie, 5 = long movie")
    era: Literal["before2000", "2000-2015", "2016+"]
    anchor_movie: str = Field(..., description="Title of one of the 5 predefined anchor movies")


class MovieResult(BaseModel):
    tconst: str
    title: str
    year: int
    runtime: int
    genres: str
    rating: float
    match_percent: float


class ClusterAnalytics(BaseModel):
    cluster_id: int
    cluster_name: str
    avg_rating: float
    top_genres: List[str]
    era_distribution: Dict[str, float]


class RecommendResponse(BaseModel):
    cluster: ClusterAnalytics
    movies: List[MovieResult]
