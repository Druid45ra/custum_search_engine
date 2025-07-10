from indexer.indexer import Indexer


def test_indexer_connection():
    indexer = Indexer("http://localhost:9200")
    assert indexer.es.ping()
