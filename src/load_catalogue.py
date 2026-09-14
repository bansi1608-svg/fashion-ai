# load_catalogue.py

import json

# "r" means "read mode"
with open("data/sample_catalogue.json", "r") as f:
    catalogue = json.load(f)

print(f"Loaded {len(catalogue)} products from file:\n")
for product in catalogue:
    print(f"- {product['name']} (₹{product['price']})")