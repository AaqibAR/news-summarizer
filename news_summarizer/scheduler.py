"""
scheduler.py
------------
Runs the news summarizer automatically every day at a set time.
"""

import schedule
import time
from datetime import datetime

from news_summarizer.fetcher import fetch_headlines
from news_summarizer.summarizer import summarize_all
from news_summarizer.digest import format_digest, save_digest


CATEGORIES = ["technology", "business", "science"]
ARTICLES_PER_CATEGORY = 5
RUN_AT = "08:00"


def run_digest():
    """Fetch, summarize and save digest for all categories."""
    print(f"\n🤖 Running News Summarizer — {datetime.now().strftime('%B %d, %Y %H:%M')}")
    print("=" * 60)

    for category in CATEGORIES:
        print(f"\n📂 Category: {category.upper()}")
        try:
            articles = fetch_headlines(category=category, page_size=ARTICLES_PER_CATEGORY)
            articles = summarize_all(articles)
            content  = format_digest(articles, category=category)
            path     = save_digest(content, category=category)
            print(f"  ✅ Saved: {path}")
        except Exception as e:
            print(f"  ❌ Failed for {category}: {e}")

    print("\n🎉 All digests complete!\n")


def start_scheduler():
    """Schedule the digest to run daily at RUN_AT time."""
    print(f"⏰ Scheduler started — digest will run daily at {RUN_AT}")
    print("   Press Ctrl+C to stop.\n")

    schedule.every().day.at(RUN_AT).do(run_digest)

    while True:
        schedule.run_pending()
        time.sleep(60)