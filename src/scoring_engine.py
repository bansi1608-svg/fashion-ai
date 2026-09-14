# scoring_engine.py
#
# Reusable scoring/ranking logic for our recommendation engine.
# Designed to be imported by other scripts (e.g. recommend_from_db.py)
# without re-running the demo code at the bottom.

def score_product(product, style, colour, category, budget):
    """
    Scores one product against the user's request.
    Returns a score from 0 to 100.

    Weights (from our project plan):
        Style match     40%
        Colour match    20%
        Category match  20%
        Price/value     20%

    Note: style_tags is a LIST (a product can match multiple aesthetics),
    so we check membership with "in" instead of exact equality.
    """
    style_score = 40 if style in product["style_tags"] else 0
    colour_score = 20 if product["colour"] == colour else 0
    category_score = 20 if product["category"] == category else 0
    price_score = 20 if product["price"] <= budget else 0

    return style_score + colour_score + category_score + price_score


def recommend_products(catalogue, style, colour, category, budget):
    """
    Scores every product in the catalogue and returns them
    sorted from best match to worst match.
    """
    scored_products = []

    for product in catalogue:
        score = score_product(product, style, colour, category, budget)
        product_with_score = dict(product)
        product_with_score["match_score"] = score
        scored_products.append(product_with_score)

    ranked = sorted(scored_products, key=lambda p: p["match_score"], reverse=True)
    return ranked


if __name__ == "__main__":
    # Demo using sample/test data - only runs when this file is executed
    # directly (python3 src/scoring_engine.py), NOT when another script
    # imports recommend_products from it.
    sample_catalogue = [
        {"name": "Sample Black Top", "price": 699, "category": "top", "colour": "black", "style_tags": ["baddie"]},
        {"name": "Sample Red Top", "price": 799, "category": "top", "colour": "red", "style_tags": ["baddie"]},
        {"name": "Sample Baggy Jeans", "price": 999, "category": "bottom", "colour": "blue", "style_tags": ["streetwear"]},
        {"name": "Sample Silver Necklace", "price": 299, "category": "accessory", "colour": "silver", "style_tags": ["baddie"]},
        {"name": "Sample White Sneakers", "price": 1499, "category": "shoes", "colour": "white", "style_tags": ["old money"]},
        {"name": "Sample Black Crop Top", "price": 1050, "category": "top", "colour": "black", "style_tags": ["baddie", "streetwear"]},
    ]

    results = recommend_products(
        catalogue=sample_catalogue,
        style="baddie",
        colour="black",
        category="top",
        budget=1000
    )

    print("Ranked recommendations for: baddie / black / top / under ₹1000\n")
    for product in results:
        print(f"{product['match_score']}% match — {product['name']} (₹{product['price']})")