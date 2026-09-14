# save_catalogue.py
#
# NOTE: sample_catalogue is still SAMPLE/TEST data. Not real products.

import json

sample_catalogue = [
    {"name": "Sample Black Top", "price": 699, "category": "top", "colour": "black", "style": "baddie"},
    {"name": "Sample Baggy Jeans", "price": 999, "category": "bottom", "colour": "blue", "style": "streetwear"},
    {"name": "Sample Silver Necklace", "price": 299, "category": "accessory", "colour": "silver", "style": "baddie"},
    {"name": "Sample White Sneakers", "price": 1499, "category": "shoes", "colour": "white", "style": "old money"},
]

# "w" means "write mode" — creates the file if it doesn't exist,
# or overwrites it if it does.
with open("data/sample_catalogue.json", "w") as f:
    json.dump(sample_catalogue, f, indent=2)

print("Saved catalogue to data/sample_catalogue.json")