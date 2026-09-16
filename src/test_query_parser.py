# test_query_parser.py
#
# Quick manual tests for parse_query, run against your REAL catalogue.

from src.recommend_from_db import fetch_all_products
from src.query_parser import parse_query

test_queries = [
    "baddie outfit under ₹2500",
    "black top under 1000",
    "something streetwear",
    "cheap shoes",  # deliberately testing an unrecognized word
]

catalogue = fetch_all_products()

for query in test_queries:
    result = parse_query(query, catalogue)
    print(f"Query: {query!r}")
    print(f"  -> {result}\n")