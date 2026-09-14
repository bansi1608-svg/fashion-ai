# validate_catalogue.py
#
# Checks our real catalogue for missing or malformed fields
# before the data reaches a database.

import json

REQUIRED_FIELDS = [
    "name",
    "price",
    "currency",
    "category",
    "colour",
    "description",
    "brand",
    "brand_website",
    "product_url",
    "availability",
    "style_tags"
]

with open("data/real_catalogue.json", "r") as f:
    catalogue = json.load(f)

print(f"Loaded {len(catalogue)} products.\n")

total_issues = 0

for index, product in enumerate(catalogue):
    issues = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        value = product.get(field)

        if value is None or value == "":
            issues.append(f"missing/empty '{field}'")

    # Check price is a number
    if not isinstance(product.get("price"), (int, float)):
        issues.append("price is not a number")

    # Check style_tags is a list
    if not isinstance(product.get("style_tags"), list):
        issues.append(
            'style_tags should be a list, e.g. ["streetwear", "casual"]'
        )

    # Check availability has an allowed value
    if product.get("availability") not in ["in_stock", "out_of_stock"]:
        issues.append(
            "availability must be 'in_stock' or 'out_of_stock'"
        )

    # Print issues for this product
    if issues:
        total_issues += len(issues)

        print(
            f"Product {index + 1} "
            f"({product.get('name', 'UNKNOWN')}):"
        )

        for issue in issues:
            print(f"  - {issue}")

if total_issues == 0:
    print("All products passed validation.")
    print("Catalogue is ready for the next milestone.")
else:
    print(
        f"\nTotal issues found: {total_issues}."
    )
    print(
        "Fix these in data/real_catalogue.json "
        "and run the validator again."
    )