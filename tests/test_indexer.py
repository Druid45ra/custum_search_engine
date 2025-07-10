import pytest
from indexer.indexer import Indexer


def test_process_text():
    indexer = Indexer()
    text = "This is a test document."
    tokens = indexer.process_text(text)
    assert tokens == ["test", "document"]


def test_tfidf():
    indexer = Indexer()
    docs = [
        {"url": "test1", "title": "Test", "text": "test document one"},
        {"url": "test2", "title": "Test2", "text": "test document two"},
    ]
    tfidf_docs = indexer.calculate_tfidf(docs)
    assert len(tfidf_docs) == 2
    assert "test" in tfidf_docs[0]["tfidf"]
