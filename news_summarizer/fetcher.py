"""
fetcher.py
----------
Fetches top news headlines from NewsAPI.
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"


def fetch_headlines(category: str = "technology", country: str = "us", page_size: int = 5) -> list[dict]:
    """
    Fetch top headlines from NewsAPI.

    Args:
        category: News category (technology, business, health, sports, science)
        country: Country code (us, gb, au etc.)
        page_size: Number of articles to fetch

    Returns:
        List of article dicts with title, description, url, source
    """
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found in .env file")

    params = {
        "apiKey": NEWS_API_KEY,
        "category": category,
        "country": country,
        "pageSize": page_size,
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    if data["status"] != "ok":
        raise RuntimeError(f"NewsAPI error: {data.get('message', 'Unknown error')}")

    articles = []
    for item in data["articles"]:
        articles.append({
            "title":       item.get("title", "No title"),
            "description": item.get("description", "No description"),
            "url":         item.get("url", ""),
            "source":      item.get("source", {}).get("name", "Unknown"),
        })

    return articles