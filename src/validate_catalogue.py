# validate_catalogue.py
#
# Checks our real catalogue for missing/malformed required fields.
# image_url is now REQUIRED (was optional through Milestone 11) -
# visual search (Milestone 12) can't function without it.

import json

REQUIRED_FIELDS = [
    "name", "price", "currency", "category", "colour",
    "description", "brand", "brand_website", "product_url",
    "image_url", "availability", "style_tags"
]

with open("data/real_catalogue.json", "r") as f:
    catalogue = json.load(f)

print(f"Loaded {len(catalogue)} products.\n")

total_issues = 0
missing_images = 0

for index, product in enumerate(catalogue):
    issues = []

    for field in REQUIRED_FIELDS:
        value = product.get(field)
        if value is None or value == "" or value == "REPLACE":
            issues.append(f"missing/placeholder '{field}'")
            if field == "image_url":
                missing_images += 1

    if not isinstance(product.get("price"), (int, float)):
        issues.append("price is not a number")

    if not isinstance(product.get("style_tags"), list):
        issues.append("style_tags should be a list, e.g. [\"baddie\"]")

    if issues:
        total_issues += len(issues)
        print(f"Product {index} ({product.get('name', 'UNKNOWN')}):")
        for issue in issues:
            print(f"  - {issue}")

if total_issues == 0:
    print("All products passed validation.")
else:
    print(f"\nTotal issues found: {total_issues} ({missing_images} missing image_url).")
    print("Products missing image_url will simply be skipped during image")
    print("embedding generation next chunk - not a blocker, just a heads up.")