# scoring_engine.py
#
# NOTE: sample_catalogue below is still SAMPLE/TEST data for practicing
# logic. Not real brands, prices, or products.

sample_catalogue = [
    {"name": "Sample Black Top", "price": 699, "category": "top", "colour": "black", "style": "baddie"},
    {"name": "Sample Red Top", "price": 799, "category": "top", "colour": "red", "style": "baddie"},
    {"name": "Sample Baggy Jeans", "price": 999, "category": "bottom", "colour": "blue", "style": "streetwear"},
    {"name": "Sample Silver Necklace", "price": 299, "category": "accessory", "colour": "silver", "style": "baddie"},
    {"name": "Sample White Sneakers", "price": 1499, "category": "shoes", "colour": "white", "style": "old money"},
    {"name": "Sample Black Crop Top", "price": 1050, "category": "top", "colour": "black", "style": "baddie"},
]


def score_product(product, style, colour, category, budget):
    """
    Scores one product against the user's request.
    Returns a score from 0 to 100.

    Weights (from our project plan):
        Style match     40%
        Colour match    20%
        Category match  20%
        Price/value     20%
    """
    # Each match is True (1) or False (0), multiplied by its weight
    style_score = 40 if product["style"] == style else 0
    colour_score = 20 if product["colour"] == colour else 0
    category_score = 20 if product["category"] == category else 0

    # Price/value score: full 20 points if within budget,
    # 0 points if over budget. (We can make this smarter later.)
    if product["price"] <= budget:
        price_score = 20
    else:
        price_score = 0

    total_score = style_score + colour_score + category_score + price_score
    return total_score


def recommend_products(catalogue, style, colour, category, budget):
    """
    Scores every product in the catalogue and returns them
    sorted from best match to worst match.
    """
    scored_products = []

    for product in catalogue:
        score = score_product(product, style, colour, category, budget)
        # We attach the score onto a copy of the product dict so we can
        # display it later.
        product_with_score = product.copy()
        product_with_score["match_score"] = score
        scored_products.append(product_with_score)

    # Sort by match_score, highest first.
    # key=lambda p: p["match_score"] tells sorted() what value to sort by.
    # reverse=True means highest score comes first.
    ranked = sorted(scored_products, key=lambda p: p["match_score"], reverse=True)

    return ranked


# --- Try it out ---
results = recommend_products(
    catalogue=sample_catalogue,
    style="baddie",
    colour="black",
    category="top",
    budget=500
)

print("Ranked recommendations for: baddie / black / top / under ₹1000\n")
for product in results:
    print(f"{product['match_score']}% match — {product['name']} (₹{product['price']})")