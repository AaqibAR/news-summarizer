"""
tests/test_news_summarizer.py
-----------------------------
Unit tests for News Summarizer Bot.
Run with: pytest tests/
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from news_summarizer.fetcher import fetch_headlines
from news_summarizer.summarizer import summarize_article
from news_summarizer.digest import format_digest, save_digest


# ── Fetcher ───────────────────────────────────────────────────────────────────

class TestFetcher:
    @patch("news_summarizer.fetcher.requests.get")
    def test_fetch_returns_articles(self, mock_get):
        mock_get.return_value.raise_for_status = MagicMock()
        mock_get.return_value.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "title": "Test Article",
                    "description": "Test description",
                    "url": "https://example.com",
                    "source": {"name": "Test Source"},
                }
            ],
        }
        articles = fetch_headlines(page_size=1)
        assert len(articles) == 1
        assert articles[0]["title"] == "Test Article"
        assert articles[0]["source"] == "Test Source"

    @patch("news_summarizer.fetcher.requests.get")
    def test_fetch_raises_on_api_error(self, mock_get):
        mock_get.return_value.raise_for_status = MagicMock()
        mock_get.return_value.json.return_value = {
            "status": "error",
            "message": "Invalid API key"
        }
        with pytest.raises(RuntimeError):
            fetch_headlines()

    def test_fetch_raises_without_api_key(self):
        with patch("news_summarizer.fetcher.NEWS_API_KEY", None):
            with pytest.raises(ValueError):
                fetch_headlines()


# ── Summarizer ────────────────────────────────────────────────────────────────

class TestSummarizer:
    @patch("news_summarizer.summarizer.client")
    def test_summarize_returns_string(self, mock_client):
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="  This is a summary.  "))
        ]
        result = summarize_article("Test Title", "Test description")
        assert isinstance(result, str)
        assert result == "This is a summary."

    def test_summarize_no_description(self):
        result = summarize_article("Test Title", "No description")
        assert "No description" in result


# ── Digest ────────────────────────────────────────────────────────────────────

class TestDigest:
    @pytest.fixture
    def sample_articles(self):
        return [
            {
                "title": "Article One",
                "source": "Source A",
                "url": "https://example.com/1",
                "summary": "Summary of article one.",
            },
            {
                "title": "Article Two",
                "source": "Source B",
                "url": "https://example.com/2",
                "summary": "Summary of article two.",
            },
        ]

    def test_format_digest_contains_title(self, sample_articles):
        content = format_digest(sample_articles, category="technology")
        assert "TECHNOLOGY" in content
        assert "Article One" in content
        assert "Article Two" in content

    def test_format_digest_contains_summaries(self, sample_articles):
        content = format_digest(sample_articles, category="technology")
        assert "Summary of article one." in content
        assert "Summary of article two." in content

    def test_save_digest_creates_file(self, sample_articles, tmp_path):
        content = format_digest(sample_articles)
        with patch("news_summarizer.digest.OUTPUT_DIR", tmp_path):
            path = save_digest(content, category="technology")
            assert Path(path).exists()