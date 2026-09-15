# recommend_from_db.py
#
# Fetches all products from PostgreSQL and ranks them using our
# scoring logic against a user's search request.

import psycopg
from psycopg.rows import dict_row
from src.scoring_engine import recommend_products

DB_CONNECTION = "dbname=fashionai"


def fetch_all_products():
    with psycopg.connect(DB_CONNECTION, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products;")
            return cur.fetchall()


def main():
    catalogue = fetch_all_products()
    print(f"Fetched {len(catalogue)} products from the database.\n")

    # EDIT these values to match style_tags/colours/categories that
    # actually exist in YOUR real_catalogue.json
    results = recommend_products(
        catalogue=catalogue,
        style="baddie",
        colour="black",
        category="top",
        budget=1000
    )

    print("Ranked recommendations:\n")
    for product in results:
        print(f"{product['match_score']}% match — {product['name']} (₹{product['price']}) [{product['brand']}]")


if __name__ == "__main__":
    main()