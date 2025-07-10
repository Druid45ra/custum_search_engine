Custom Search Engine
A lightweight search engine built in Python, featuring web crawling, indexing, and a search API. The project is designed for simplicity and extensibility, with modular components for crawling websites, indexing content, and serving search queries via a RESTful API.
Features

Crawler: Recursively crawls websites starting from a given URL, respects robots.txt, and extracts relevant content (title, text, URLs) up to a configurable limit.
Indexer: Processes text using NLTK for tokenization and stopword removal, calculates TF-IDF scores, and stores documents in Elasticsearch for efficient retrieval.
Search API: A Flask-based API with endpoints for searching (GET /search?q=term) and initiating crawls (POST /crawl), returning relevance-ranked results.
Tests: Unit and functional tests for crawling, indexing, and API functionality.

Project Structure
custom_search_engine/
│
├── crawler/
│   ├── crawler.py          # Crawling logic and Crawler class
│   ├── utils.py            # Helper functions: URL validation, robots.txt parsing
├── indexer/
│   ├── indexer.py          # Text processing, TF-IDF calculation, Elasticsearch indexing
├── api/
│   ├── app.py              # Flask app setup
│   ├── routes.py           # API endpoint definitions
├── config/
│   ├── settings.py         # Configuration (Elasticsearch host, start URL, crawl limit)
├── tests/
│   ├── test_crawler.py     # Tests for crawler
│   ├── test_indexer.py     # Tests for indexer
│   ├── test_api.py         # Tests for API
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── main.py                 # Main script to run crawler and indexer
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation

Requirements

Python 3.9+
Elasticsearch 8.15.0 (running locally or accessible via host)
Docker (optional, for running Elasticsearch)
NLTK data (punkt, punkt_tab, stopwords)

Setup

Clone the repository:
git clone <repository-url>
cd custom_search_engine


Set up a virtual environment:
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows


Install dependencies:
pip install -r requirements.txt


Download NLTK data:
python -m nltk.downloader punkt punkt_tab stopwords


Configure environment variables:Copy .env.example to .env and edit as needed:
cp .env.example .env

Example .env:
ELASTICSEARCH_HOST=http://localhost:9200
START_URL=https://www.wikipedia.org
CRAWL_LIMIT=10


Run Elasticsearch:Start Elasticsearch using Docker:
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.15.0

Verify it’s running:
curl http://localhost:9200



Usage

Run the crawler and indexer:
python main.py

This crawls the START_URL, extracts content, and indexes it in Elasticsearch.
Example output:
Crawled: https://www.wikipedia.org, Title: Wikipedia
Crawled: https://www.wikipedia.org/portal, Title: Wikipedia Portal
...
Total pages crawled: 10
Indexed 10 pages to Elasticsearch


Start the API:
python api/app.py


Search via API:Query the search endpoint:
curl "http://localhost:5000/search?q=wikipedia"

Example response:
{
    "results": [
        {"url": "https://www.wikipedia.org", "title": "Wikipedia", "score": 1.23},
        ...
    ]
}


Trigger a crawl via API:
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.wikipedia.org"}' http://localhost:5000/crawl

Example response:
{"message": "Crawled and indexed 10 pages"}


Run tests:
pytest tests/



Development Stages

Setup: Initialize Git repo, virtual environment, and install dependencies.
Basic Crawler: Crawl a single page and parse HTML content.
Recursive Crawler: Extend to recursive crawling with robots.txt support and crawl limits.
Indexer: Implement text processing, TF-IDF calculation, and Elasticsearch indexing.
API: Create Flask API with search and crawl endpoints.
Tests & Docs: Write unit tests and comprehensive documentation.

Notes

Scalability: For large-scale crawling, consider adding a task queue like Celery.
Error Handling: The crawler handles network errors and invalid URLs but can be extended for robustness.
Search Enhancements: Add pagination or filters to the /search endpoint for better usability.

Contributing
Feel free to submit issues or pull requests to improve the project. Ensure tests pass and follow the coding style in existing files.
License
This project is licensed under the MIT License.
