from flask import Blueprint, request, jsonify
from elasticsearch import Elasticsearch
import os

search_bp = Blueprint("search", __name__)
es = Elasticsearch([os.getenv("ES_HOST", "http://localhost:9200")])


@search_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    res = es.search(
        index="documents",
        query={"multi_match": {"query": query, "fields": ["content"]}},
    )
    hits = res["hits"]["hits"]
    results = [{"url": hit["_source"]["url"], "score": hit["_score"]} for hit in hits]
    return jsonify(results)
