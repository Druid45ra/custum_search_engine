from elasticsearch import Elasticsearch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import math
from config.settings import ELASTICSEARCH_HOST


class Indexer:
    def __init__(self):
        self.es = Elasticsearch([ELASTICSEARCH_HOST])
        self.stop_words = set(stopwords.words("english"))
        self.documents = []

    def process_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t.isalnum() and t not in self.stop_words]
        return tokens

    def calculate_tfidf(self, docs):
        tf = []
        df = Counter()
        for doc in docs:
            tokens = self.process_text(doc["text"])
            term_counts = Counter(tokens)
            tf.append(term_counts)
            for term in term_counts:
                df[term] += 1

        tfidf_docs = []
        N = len(docs)
        for i, doc in enumerate(docs):
            tfidf = {}
            for term, count in tf[i].items():
                tf_score = count / sum(tf[i].values())
                idf_score = math.log(N / (df[term] + 1))
                tfidf[term] = tf_score * idf_score
            tfidf_docs.append(
                {"url": doc["url"], "title": doc["title"], "tfidf": tfidf}
            )
        return tfidf_docs

    def index_documents(self, docs):
        tfidf_docs = self.calculate_tfidf(docs)
        if not self.es.indices.exists(index="web_pages"):
            self.es.indices.create(index="web_pages")
        for doc in tfidf_docs:
            self.es.index(
                index="web_pages",
                body={"url": doc["url"], "title": doc["title"], "tfidf": doc["tfidf"]},
            )


if __name__ == "__main__":
    from crawler.crawler import crawl_recursive

    indexer = Indexer()
    pages = crawl_recursive(START_URL)
    indexer.index_documents(pages)
