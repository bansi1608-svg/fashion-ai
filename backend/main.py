# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.recommend_from_db import fetch_all_products
from src.scoring_engine import recommend_products

app = FastAPI(title="Fashion Discovery API")

# Allow our Next.js frontend (running on a different port) to call this API.
# Without this, the browser blocks the request entirely for security reasons.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/products")
def get_products():
    return fetch_all_products()


class RecommendRequest(BaseModel):
    style: str
    colour: str
    category: str
    budget: float


@app.post("/recommend")
def recommend(request: RecommendRequest):
    catalogue = fetch_all_products()
    results = recommend_products(
        catalogue=catalogue,
        style=request.style,
        colour=request.colour,
        category=request.category,
        budget=request.budget,
    )
    return results