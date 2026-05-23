# 📰 News Summarizer Bot

An AI-powered Python CLI bot that fetches top news headlines,
summarizes them using Groq AI, and saves a clean daily digest
to a file — automatically.

---

## Features

- 🌍 Fetches live headlines from NewsAPI
- 🤖 Summarizes articles using Groq AI (LLaMA 3)
- 📂 Saves clean daily digests to output/ folder
- 🗂️ Supports multiple categories (technology, business, science)
- ⏰ Built-in daily scheduler
- ✅ Unit tested with pytest

---

## Project Structure

news-summarizer/
├── news_summarizer/
│   ├── init.py
│   ├── fetcher.py       # Fetch headlines from NewsAPI
│   ├── summarizer.py    # Summarize articles with Groq AI
│   ├── digest.py        # Format and save daily digest
│   └── scheduler.py     # Run automatically daily
├── output/              # Saved digests go here
├── tests/
│   └── test_news_summarizer.py
├── main.py
├── requirements.txt
└── README.md

---

## Getting Started

### 1. Clone and install dependencies

```bash
git clone https://github.com/AaqibAR/news-summarizer.git
cd news-summarizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up API keys

Create a `.env` file in the root:

NEWS_API_KEY=your_newsapi_key_here
GROQ_API_KEY=your_groq_api_key_here

Get your keys from:
- NewsAPI → newsapi.org
- Groq → console.groq.com

### 3. Run the bot

```bash
# Fetch and summarize technology news
python3 main.py --run

# Choose a different category
python3 main.py --run --category business

# Fetch more articles
python3 main.py --run --category science --size 10

# Run automatically every day at 08:00
python3 main.py --schedule
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Tech Stack

- `requests` — fetch news from NewsAPI
- `groq` — AI summaries using LLaMA 3
- `python-dotenv` — manage API keys safely
- `schedule` — daily automation
- `pytest` — unit testing

---

## License

MIT