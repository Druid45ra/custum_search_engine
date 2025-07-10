from dotenv import load_dotenv
import os

load_dotenv()

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
START_URL = os.getenv("START_URL", "https://www.wikipedia.org")
CRAWL_LIMIT = int(os.getenv("CRAWL_LIMIT", 10))
