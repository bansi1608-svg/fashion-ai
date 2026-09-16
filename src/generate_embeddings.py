# generate_embeddings.py
#
# Generates a real semantic embedding for every product using a
# pretrained model, and stores it in the database.

import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

DB_CONNECTION = "dbname=fashionai"


def build_embedding_text(product):
    """
    Combines several fields into one rich piece of text for embedding.
    Embedding just the product name alone would lose a lot of meaning -
    this way, category, colour, brand, and style all contribute.
    """
    style_tags = ", ".join(product["style_tags"]) if product["style_tags"] else ""

    parts = [
        product["name"],
        product["description"] or "",
        f"Category: {product['category']}",
        f"Colour: {product['colour']}",
        f"Brand: {product['brand']}",
        f"Style: {style_tags}" if style_tags else "",
    ]
    # Join only the non-empty parts
    return ". ".join(part for part in parts if part)


def main():
    print("Loading embedding model (first run downloads it, roughly 90MB)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with psycopg.connect(DB_CONNECTION, row_factory=dict_row) as conn:
        register_vector(conn)  # teaches this connection how to send/receive vectors

        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, description, category, colour, brand, style_tags FROM products;"
            )
            products = cur.fetchall()

        print(f"Generating embeddings for {len(products)} products...\n")

        with conn.cursor() as cur:
            for product in products:
                text = build_embedding_text(product)
                embedding = model.encode(text)
                cur.execute(
                    "UPDATE products SET embedding = %s WHERE id = %s",
                    (embedding, product["id"]),
                )
                print(f"  done: {product['name']}")

        conn.commit()

    print("\nAll products now have embeddings.")


if __name__ == "__main__":
    main()