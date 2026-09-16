# generate_image_embeddings.py
#
# Downloads each product's real image and generates a CLIP embedding
# for it. Products with a missing or broken image_url are skipped
# with a message, not crashed on - real-world image URLs aren't
# always reliable.

import io
import time

import requests
from PIL import Image
import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

DB_CONNECTION = "dbname=fashionai"
REQUEST_TIMEOUT = 10          # seconds to wait for an image to download
DELAY_BETWEEN_REQUESTS = 0.5  # seconds - be polite to brand websites' servers


def download_image(url):
    """
    Downloads an image from a URL and returns it as a PIL Image
    (converted to RGB), or None if anything goes wrong.
    """
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        return image.convert("RGB")
    except Exception as e:
        print(f"    could not load image ({e})")
        return None


def main():
    print("Loading CLIP model (first run downloads it, a few hundred MB)...")
    model = SentenceTransformer("clip-ViT-B-32")

    with psycopg.connect(DB_CONNECTION, row_factory=dict_row) as conn:
        register_vector(conn)

        with conn.cursor() as cur:
            cur.execute("SELECT id, name, image_url FROM products;")
            products = cur.fetchall()

        print(f"Processing {len(products)} products...\n")

        succeeded = 0
        skipped = 0

        with conn.cursor() as cur:
            for product in products:
                print(f"  {product['name']}")

                if not product["image_url"]:
                    print("    no image_url, skipping")
                    skipped += 1
                    continue

                image = download_image(product["image_url"])
                if image is None:
                    skipped += 1
                    continue

                embedding = model.encode(image)
                cur.execute(
                    "UPDATE products SET image_embedding = %s WHERE id = %s",
                    (embedding, product["id"]),
                )
                succeeded += 1
                time.sleep(DELAY_BETWEEN_REQUESTS)

        conn.commit()

    print(f"\nDone. {succeeded} image embeddings generated, {skipped} skipped.")


if __name__ == "__main__":
    main()