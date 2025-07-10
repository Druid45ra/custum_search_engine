import pytest
from crawler.crawler import crawl_page
from crawler.utils import is_valid_url


def test_crawl_page():
    result = crawl_page("https://example.com")
    assert result is not None
    assert result["url"] == "https://example.com"
    assert result["title"] is not None
    assert len(result["text"]) > 0


def test_valid_url():
    assert is_valid_url("https://example.com") is True
    assert is_valid_url("https://invalid-url") is False
