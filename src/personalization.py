# personalization.py
#
# Looks at a session's past interactions and infers a likely
# style/colour/category preference - ONLY when there's enough
# history to make that a reasonable inference, not a guess from
# a single data point.

from collections import Counter

import psycopg
from psycopg.rows import dict_row

DB_CONNECTION = "dbname=fashionai"

# Require at least this many matching past interactions before we
# trust a preference enough to use it. Prevents inferring a "favorite"
# from one search that might have been a one-off.
MIN_INTERACTIONS_FOR_PREFERENCE = 2


def get_user_preferences(session_id):
    """
    Returns a dict like {"style": "baddie"} for any field that has
    enough history to support a confident inference. Missing keys
    mean "not enough data" for that field - never a guess.
    """
    if not session_id:
        return {}

    with psycopg.connect(DB_CONNECTION, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT style, colour, category FROM user_interactions WHERE session_id = %s",
                (session_id,),
            )
            rows = cur.fetchall()

    styles = Counter(r["style"] for r in rows if r["style"])
    colours = Counter(r["colour"] for r in rows if r["colour"])
    categories = Counter(r["category"] for r in rows if r["category"])

    preferences = {}
    if sum(styles.values()) >= MIN_INTERACTIONS_FOR_PREFERENCE:
        preferences["style"] = styles.most_common(1)[0][0]
    if sum(colours.values()) >= MIN_INTERACTIONS_FOR_PREFERENCE:
        preferences["colour"] = colours.most_common(1)[0][0]
    if sum(categories.values()) >= MIN_INTERACTIONS_FOR_PREFERENCE:
        preferences["category"] = categories.most_common(1)[0][0]

    return preferences