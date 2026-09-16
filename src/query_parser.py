# query_parser.py
#
# A simple, RULE-BASED (not machine learning) parser that extracts
# structured search criteria from a free-text query like:
#   "baddie outfit under ₹2500"
#
# This is our first step into "AI fashion understanding" - an
# explainable baseline before we introduce real ML (embeddings)
# in Milestone 11.

import re


def extract_budget(text):
    """
    Finds a number in the text (handles both "2500" and "2,500")
    and returns it as an integer. Returns None if no number found.
    """
    # IMPORTANT: the comma-grouped branch requires AT LEAST ONE comma
    # group (the trailing '+' not '*'). Using '*' here is a common bug -
    # it lets the plain-digit branch match and stop after just the first
    # 3 digits (e.g. truncating "2500" down to "250"), since regex
    # alternation accepts the first branch that succeeds, not the
    # longest one.
    match = re.search(r'₹?\s*(\d{1,3}(?:,\d{3})+|\d+)', text)
    if match:
        number_str = match.group(1).replace(",", "")
        return int(number_str)
    return None


def build_vocab(catalogue):
    """
    Builds sets of known styles, colours, and categories directly from
    the ACTUAL product data - so the parser only ever recognizes words
    that genuinely exist in our catalogue, never guesses or invents one.
    """
    styles = set()
    colours = set()
    categories = set()

    for product in catalogue:
        for tag in product["style_tags"]:
            styles.add(tag.lower())
        colours.add(product["colour"].lower())
        categories.add(product["category"].lower())

    return styles, colours, categories


def parse_query(text, catalogue):
    """
    Extracts style, colour, category, and budget from a free-text query.
    Any field that can't be confidently found is returned as None.
    """
    text_lower = text.lower()
    styles, colours, categories = build_vocab(catalogue)

    found_style = next((s for s in styles if s in text_lower), None)
    found_colour = next((c for c in colours if c in text_lower), None)
    found_category = next((c for c in categories if c in text_lower), None)
    budget = extract_budget(text_lower)

    return {
        "style": found_style,
        "colour": found_colour,
        "category": found_category,
        "budget": budget,
    }