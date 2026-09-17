# backend/main.py

import io
from fastapi import UploadFile, File
from PIL import Image
from src.visual_search import visual_search

from src.personalization import get_user_preferences

from typing import Optional
from src.interactions import log_interaction

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
    session_id: Optional[str] = None


@app.post("/search")
def search(request: SearchRequest):
    """
    Parses the query, then fills in any UNDETECTED fields using the
    session's past preferences (if there's enough history) - never
    overriding anything the user actually typed.
    """
    catalogue = fetch_all_products()
    parsed = parse_query(request.query, catalogue)

    preferences = get_user_preferences(request.session_id)

    applied_style = parsed["style"] or preferences.get("style")
    applied_colour = parsed["colour"] or preferences.get("colour")
    applied_category = parsed["category"] or preferences.get("category")
    budget = parsed["budget"] if parsed["budget"] is not None else float("inf")

    personalization_used = (
        applied_style != parsed["style"]
        or applied_colour != parsed["colour"]
        or applied_category != parsed["category"]
    )

    results = recommend_products(
        catalogue=catalogue,
        style=applied_style,
        colour=applied_colour,
        category=applied_category,
        budget=budget,
    )

    return {
        "parsed_query": parsed,
        "applied_query": {
            "style": applied_style,
            "colour": applied_colour,
            "category": applied_category,
        },
        "personalization_used": personalization_used,
        "results": results,
    }

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

class InteractionRequest(BaseModel):
    session_id: str
    interaction_type: str
    style: Optional[str] = None
    colour: Optional[str] = None
    category: Optional[str] = None
    product_id: Optional[int] = None


@app.post("/interactions")
def record_interaction(request: InteractionRequest):
    log_interaction(
        session_id=request.session_id,
        interaction_type=request.interaction_type,
        style=request.style,
        colour=request.colour,
        category=request.category,
        product_id=request.product_id,
    )
    return {"status": "logged"}
