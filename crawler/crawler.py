import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from .utils import is_valid_url, get_robots_parser
import logging


class Crawler:
    def __init__(self, start_url, max_depth=2):
        self.start_url = start_url
        self.max_depth = max_depth
        self.visited = set()
        self.logger = logging.getLogger(__name__)

    def crawl(self, url=None, depth=0):
        if url is None:
            url = self.start_url

        if depth > self.max_depth:
            return

        if url in self.visited:
            return

        if not is_valid_url(url):
            return

        self.visited.add(url)
        self.logger.info(f"Crawling: {url}")

        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text()

            # TODO: Trimite textul la indexer aici

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if self._same_domain(next_url):
                    self.crawl(next_url, depth + 1)

        except Exception as e:
            self.logger.error(f"Failed to crawl {url}: {e}")

    def _same_domain(self, url):
        return urlparse(url).netloc == urlparse(self.start_url).netloc
