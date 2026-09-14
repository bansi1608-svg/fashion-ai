# learn_python_basics.py
#
# NOTE: The products below are SAMPLE/TEST data I made up purely to
# practice Python syntax. These are NOT real brands or real prices.
# Real product data comes later in Milestone 4.

# --- A single product: a dictionary (key-value pairs) ---
product_1 = {
    "name": "Sample Black Top",
    "price": 699,
    "category": "top",
    "colour": "black",
    "style": "baddie"
}

# Accessing values by key
print("Product name:", product_1["name"])
print("Product price:", product_1["price"])

# --- A catalogue: a list of dictionaries ---
sample_catalogue = [
    {"name": "Sample Black Top", "price": 699, "category": "top", "colour": "black", "style": "baddie"},
    {"name": "Sample Baggy Jeans", "price": 999, "category": "bottom", "colour": "blue", "style": "streetwear"},
    {"name": "Sample Silver Necklace", "price": 299, "category": "accessory", "colour": "silver", "style": "baddie"},
    {"name": "Sample White Sneakers", "price": 1499, "category": "shoes", "colour": "white", "style": "old money"},
    {"name": "Sample Yellow Dress", "price": 1199, "category": "dress", "colour": "yellow", "style": "traditional"}
]

# --- Looping through the catalogue ---
print("\nAll products in catalogue:")
for product in sample_catalogue:
    print(f"- {product['name']} (₹{product['price']})")

# --- A function: reusable logic with input and output ---
def filter_by_budget(catalogue, max_price):
    """
    Takes a list of product dictionaries and a maximum price.
    Returns only the products at or under that price.
    """
    result = []
    for product in catalogue:
        if product["price"] <= max_price:
            result.append(product)
    return result

# --- Using the function ---
budget = 1500
affordable_products = filter_by_budget(sample_catalogue, budget)

print(f"\nProducts under ₹{budget}:")
for product in affordable_products:
    print(f"- {product['name']} (₹{product['price']})")