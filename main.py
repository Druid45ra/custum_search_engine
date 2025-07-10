from crawler.crawler import Crawler
from indexer.indexer import Indexer
from config import settings

import logging

# Configurare logging
logging.basicConfig(level=logging.INFO)


def index_callback(url, text, indexer):
    """Funcție callback: primește conținutul și îl trimite către indexer."""
    indexer.index_document(url, text)


def main():
    # Initializează crawlerul și indexerul
    crawler = Crawler(start_url=settings.START_URL, max_depth=settings.MAX_DEPTH)
    indexer = Indexer(es_host=settings.ES_HOST)

    # Monkey patch: adaugă indexer-ul în crawler
    def crawl_with_index(url=None, depth=0):
        if url is None:
            url = crawler.start_url

        if depth > crawler.max_depth or url in crawler.visited:
            return

        crawler.visited.add(url)
        crawler.logger.info(f"Crawling: {url}")

        try:
            import requests
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin

            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)

            index_callback(url, text, indexer)

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if crawler._same_domain(next_url):
                    crawl_with_index(next_url, depth + 1)

        except Exception as e:
            crawler.logger.error(f"Failed to crawl {url}: {e}")

    # Rulează crawling-ul cu indexare directă
    crawl_with_index()


if __name__ == "__main__":
    main()
