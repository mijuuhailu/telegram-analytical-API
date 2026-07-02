from fastapi import FastAPI
from sqlalchemy import text

from api.db import engine
from api.schemas import MessageSearchResponse
from api.queries import (
    TOP_PRODUCTS,
    CHANNEL_ACTIVITY,
    SEARCH_MESSAGES,
    VISUAL_STATS
)

app = FastAPI(title="Medical Telegram Analytics API")

@app.get("/")
def root():
    return {
        "message": "Medical Telegram Analytics API",
        "docs": "/docs",
        "endpoints": [
            "/api/reports/top-products",
            "/api/channels/{channel_name}/activity",
            "/api/search/messages",
            "/api/reports/visual-content",
        ],
    }

# 1. Top Products
@app.get("/api/reports/top-products")
def top_products(limit: int = 10):
    with engine.connect() as conn:
        result = conn.execute(text(TOP_PRODUCTS), {"limit": limit})
        return [dict(row._mapping) for row in result]


# 2. Channel Activity
@app.get("/api/channels/{channel_name}/activity")
def channel_activity(channel_name: str):
    with engine.connect() as conn:
        result = conn.execute(text(CHANNEL_ACTIVITY), {"channel_name": channel_name})
        return [dict(row._mapping) for row in result]


# 3. Search Messages
@app.get("/api/search/messages")
def search_messages(query: str, limit: int = 20):
    with engine.connect() as conn:
        result = conn.execute(
            text(SEARCH_MESSAGES),
            {"query": query, "limit": limit}
        )
        return [dict(row._mapping) for row in result]


# 4. Visual Content Stats
@app.get("/api/reports/visual-content")
def visual_content():
    with engine.connect() as conn:
        result = conn.execute(text(VISUAL_STATS))
        return [dict(row._mapping) for row in result]