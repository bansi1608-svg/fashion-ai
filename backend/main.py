# backend/main.py
#
# The entry point for our API server.

from fastapi import FastAPI
from pydantic import BaseModel

from src.recommend_from_db import fetch_all_products
from src.scoring_engine import recommend_products

app = FastAPI(title="Fashion Discovery API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/products")
def get_products():
    """
    Returns every product currently in the database.
    """
    return fetch_all_products()


class RecommendRequest(BaseModel):
    """
    Defines exactly what a POST /recommend request must contain.
    FastAPI uses this to automatically validate incoming requests -
    if a field is missing or the wrong type, it rejects the request
    with a clear error before our code even runs.
    """
    style: str
    colour: str
    category: str
    budget: float


@app.post("/recommend")
def recommend(request: RecommendRequest):
    """
    Scores and ranks all products against the given search criteria.
    """
    catalogue = fetch_all_products()
    results = recommend_products(
        catalogue=catalogue,
        style=request.style,
        colour=request.colour,
        category=request.category,
        budget=request.budget,
    )
    return results