# backend/main.py
#
# The entry point for our API server.

from fastapi import FastAPI

app = FastAPI(title="Fashion Discovery API")


@app.get("/health")
def health_check():
    """
    A simple endpoint to confirm the server is running.
    Real products/apps almost always have a /health endpoint —
    it's what monitoring tools check to know if the server is alive.
    """
    return {"status": "ok"}