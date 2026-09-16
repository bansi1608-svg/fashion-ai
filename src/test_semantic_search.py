# test_semantic_search.py
#
# Compares our OLD rule-based parser (Milestone 10) against REAL
# semantic search (Milestone 11), using queries with words the
# rule-based parser has never seen.

from semantic_search import semantic_search
from query_parser import parse_query
from recommend_from_db import fetch_all_products

tricky_queries = [
    "affordable trendy clothes",
    "something elegant and classy",
    "casual everyday wear",
]

catalogue = fetch_all_products()

for query in tricky_queries:
    print(f"Query: {query!r}\n")

    print("  Rule-based parser (Milestone 10) understood:")
    parsed = parse_query(query, catalogue)
    print(f"    {parsed}")

    print("\n  Semantic search (Milestone 11) found:")
    results = semantic_search(query, limit=3)
    for r in results:
        print(f"    {r['similarity_score']}% similar — {r['name']} (₹{r['price']}) [{r['brand']}]")

    print("\n" + "-" * 60 + "\n")