# visual_search.py
#
# Embeds an uploaded image using CLIP and finds the most visually
# similar products via pgvector cosine distance on image_embedding.

import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

DB_CONNECTION = "dbname=fashionai"

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("clip-ViT-B-32")
    return _model


def visual_search(image, limit=10):
    """
    image: an already-opened PIL.Image (RGB).
    Returns the `limit` products whose image is most visually similar,
    ranked closest-first. Products with no image_embedding are excluded.
    """
    model = get_model()
    query_embedding = model.encode(image)

    with psycopg.connect(DB_CONNECTION, row_factory=dict_row) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, price, currency, category, colour, brand,
                       product_url, image_url,
                       image_embedding <=> %s AS distance
                FROM products
                WHERE image_embedding IS NOT NULL
                ORDER BY distance ASC
                LIMIT %s;
                """,
                (query_embedding, limit),
            )
            results = cur.fetchall()

    for r in results:
        r["similarity_score"] = round(max(0, 1 - r["distance"]) * 100)

    return results