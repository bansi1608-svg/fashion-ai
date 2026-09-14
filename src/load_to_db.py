# load_to_db.py
#
# Loads data/real_catalogue.json into the products table.
# Safe to re-run: clears existing rows first, so you never end up
# with duplicate products.

import json
import psycopg

DB_CONNECTION = "dbname=fashionai"


def load_catalogue():
    with open("data/real_catalogue.json", "r") as f:
        return json.load(f)


def main():
    catalogue = load_catalogue()
    print(f"Loaded {len(catalogue)} products from JSON file.")

    with psycopg.connect(DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            # Wipe existing rows so re-running this script is always safe
            cur.execute("TRUNCATE TABLE products RESTART IDENTITY;")

            for product in catalogue:
                cur.execute(
                    """
                    INSERT INTO products
                        (name, price, currency, category, subcategory, colour,
                         description, brand, brand_website, product_url,
                         image_url, availability, style_tags)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        product["name"],
                        product["price"],
                        product["currency"],
                        product["category"],
                        product.get("subcategory") or None,
                        product["colour"],
                        product.get("description"),
                        product["brand"],
                        product.get("brand_website"),
                        product["product_url"],
                        product.get("image_url") or None,
                        product["availability"],
                        product["style_tags"],
                    ),
                )

        conn.commit()

    print(f"Successfully loaded {len(catalogue)} products into the database.")


if __name__ == "__main__":
    main()