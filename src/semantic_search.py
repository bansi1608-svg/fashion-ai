# semantic_search.py
#
# Embeds a free-text query and finds the most semantically similar
# products using pgvector's cosine distance operator (<=>).

import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

DB_CONNECTION = "dbname=fashionai"

# Loaded once and reused, rather than reloading the model on every call -
# loading it is the slow part; encoding a query with an already-loaded
# model is fast.
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def semantic_search(query_text, limit=10):
    """
    Returns the `limit` products most semantically similar to query_text,
    ranked closest-first, each with a similarity_score for display.
    """
    model = get_model()
    query_embedding = model.encode(query_text)

    with psycopg.connect(DB_CONNECTION, row_factory=dict_row) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, price, currency, category, colour, brand,
                       product_url, style_tags,
                       embedding <=> %s AS distance
                FROM products
                ORDER BY distance ASC
                LIMIT %s;
                """,
                (query_embedding, limit),
            )
            results = cur.fetchall()

    for r in results:
        # A rough, human-friendly 0-100 display number derived from
        # cosine distance. NOT a validated accuracy metric - just a
        # friendlier way to show "how close" than a raw distance value.
        r["similarity_score"] = round(max(0, 1 - r["distance"]) * 100)

    return results