# backend/main.py

import io
from fastapi import UploadFile, File
from PIL import Image
from src.visual_search import visual_search

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.semantic_search import semantic_search
from src.recommend_from_db import fetch_all_products
from src.scoring_engine import recommend_products
from src.query_parser import parse_query

app = FastAPI(title="Fashion Discovery API")

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


class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search(request: SearchRequest):
    """
    Accepts a single free-text query (e.g. "baddie outfit under ₹2500"),
    parses it into structured criteria, and returns ranked results -
    plus what we understood from the query, for transparency.
    """
    catalogue = fetch_all_products()
    parsed = parse_query(request.query, catalogue)

    # No budget mentioned in the query = no budget constraint
    budget = parsed["budget"] if parsed["budget"] is not None else float("inf")

    results = recommend_products(
        catalogue=catalogue,
        style=parsed["style"],
        colour=parsed["colour"],
        category=parsed["category"],
        budget=budget,
    )

    return {"parsed_query": parsed, "results": results}

class SemanticSearchRequest(BaseModel):
    query: str
    limit: int = 5


@app.post("/semantic-search")
def semantic_search_endpoint(request: SemanticSearchRequest):
    return semantic_search(request.query, limit=request.limit)

@app.post("/visual-search")
async def visual_search_endpoint(file: UploadFile = File(...), limit: int = 5):
    """
    Accepts an uploaded image, embeds it with CLIP, and returns the
    most visually similar real products from our catalogue.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    return visual_search(image, limit=limit)
