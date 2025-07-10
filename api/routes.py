from flask import request, jsonify
from elasticsearch import Elasticsearch
from config.settings import ELASTICSEARCH_HOST


def init_routes(app):
    es = Elasticsearch([ELASTICSEARCH_HOST])

    @app.route("/search", methods=["GET"])
    def search():
        query = request.args.get("q", "")
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400

        body = {
            "query": {"multi_match": {"query": query, "fields": ["title^2", "tfidf.*"]}}
        }
        results = es.search(index="web_pages", body=body)
        hits = [
            {
                "url": hit["_source"]["url"],
                "title": hit["_source"]["title"],
                "score": hit["_score"],
            }
            for hit in results["hits"]["hits"]
        ]
        return jsonify({"results": hits})

    @app.route("/crawl", methods=["POST"])
    def crawl():
        from crawler.crawler import crawl_recursive
        from indexer.indexer import Indexer

        data = request.get_json()
        url = data.get("url", START_URL)
        pages = crawl_recursive(url)
        indexer = Indexer()
        indexer.index_documents(pages)
        return jsonify({"message": f"Crawled and indexed {len(pages)} pages"})
