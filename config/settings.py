import os
from dotenv import load_dotenv

load_dotenv()

START_URL = os.getenv("START_URL", "https://example.com")
MAX_DEPTH = int(os.getenv("MAX_DEPTH", 2))
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
