# interactions.py
#
# Records user interactions (searches, visual searches, clicks) for
# future personalization. Deliberately simple - just an INSERT.

import psycopg

DB_CONNECTION = "dbname=fashionai"


def log_interaction(session_id, interaction_type, style=None, colour=None,
                     category=None, product_id=None):
    with psycopg.connect(DB_CONNECTION) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_interactions
                    (session_id, interaction_type, style, colour, category, product_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (session_id, interaction_type, style, colour, category, product_id),
            )
        conn.commit()