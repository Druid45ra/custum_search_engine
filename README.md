# Custom Search Engine

A simple search engine with web crawling, indexing, and search API.

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure variables.
5. Run Elasticsearch locally or provide a valid host.

## Running
- Start crawler: `python crawler/crawler.py`
- Start API: `python api/app.py`
