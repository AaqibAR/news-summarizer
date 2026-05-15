"""
summarizer.py
-------------
Summarizes news articles using Groq's AI API.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_article(title: str, description: str) -> str:
    """
    Summarize a news article using Groq AI.

    Args:
        title: Article headline
        description: Article description or snippet

    Returns:
        A clean 2-3 sentence summary
    """
    if not description or description == "No description":
        return "No description available to summarize."

    prompt = f"""You are a news summarizer. Given a headline and description, 
write a clear and concise 2-3 sentence summary in simple English.
Do not add opinions. Just summarize the facts.

Headline: {title}
Description: {description}

Summary:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()


def summarize_all(articles: list[dict]) -> list[dict]:
    """
    Summarize a list of articles.

    Args:
        articles: List of article dicts from fetcher

    Returns:
        Same list with a 'summary' key added to each article
    """
    for article in articles:
        print(f"  Summarizing: {article['title'][:60]}...")
        article["summary"] = summarize_article(
            article["title"],
            article["description"]
        )
    return articles