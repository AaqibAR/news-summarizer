"""
main.py
-------
CLI entry point for News Summarizer Bot.

Usage:
    python3 main.py --run
    python3 main.py --run --category technology
    python3 main.py --run --category business --size 10
    python3 main.py --schedule
"""

import argparse
import sys

from news_summarizer.fetcher import fetch_headlines
from news_summarizer.summarizer import summarize_all
from news_summarizer.digest import format_digest, save_digest
from news_summarizer.scheduler import start_scheduler


def parse_args():
    parser = argparse.ArgumentParser(
        description="📰 News Summarizer Bot — AI powered daily news digest.",
    )
    parser.add_argument("--run", action="store_true",
                        help="Run the summarizer once right now.")
    parser.add_argument("--category", "-c", type=str, default="technology",
                        help="News category: technology, business, science, health, sports.")
    parser.add_argument("--size", "-s", type=int, default=5,
                        help="Number of articles to fetch (default: 5).")
    parser.add_argument("--schedule", action="store_true",
                        help="Start the scheduler to run daily automatically.")
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.run and not args.schedule:
        print("❌ Please provide --run or --schedule flag.")
        print("   Example: python3 main.py --run --category technology")
        sys.exit(1)

    if args.schedule:
        start_scheduler()
        return

    if args.run:
        print(f"\n📰 Fetching {args.size} articles from category: {args.category}")
        try:
            articles = fetch_headlines(category=args.category, page_size=args.size)
            print(f"✅ Fetched {len(articles)} articles\n")

            print("🤖 Summarizing with Groq AI...")
            articles = summarize_all(articles)

            content = format_digest(articles, category=args.category)
            print("\n" + content)

            path = save_digest(content, category=args.category)
            print(f"💾 Digest saved to: {path}\n")

        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()