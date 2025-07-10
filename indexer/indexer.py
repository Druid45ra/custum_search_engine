from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
import logging


class Indexer:
    def __init__(self, es_host):
        self.es = Elasticsearch([es_host])
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.logger = logging.getLogger(__name__)

    def index_document(self, url, text):
        doc = {
            "url": url,
            "content": text,
            # Poți adăuga și scorurile TF-IDF aici dacă folosești local vectorizer
        }
        res = self.es.index(index="documents", document=doc)
        self.logger.info(f"Indexed: {url} -> {res['_id']}")
