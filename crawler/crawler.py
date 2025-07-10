import requests
from bs4 import BeautifulSoup
from crawler.utils import is_valid_url, clean_url, is_same_domain, parse_html, can_crawl
from config.settings import START_URL, CRAWL_LIMIT
from queue import Queue


class Crawler:
    def __init__(self, start_url=START_URL, crawl_limit=CRAWL_LIMIT):
        self.start_url = start_url
        self.crawl_limit = crawl_limit

    def crawl_page(self, url):
        if not is_valid_url(url):
            print(f"Invalid URL: {url}")
            return None
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            title, text = parse_html(response.text)
            return {"url": url, "title": title, "text": text}
        except requests.RequestException as e:
            print(f"Error crawling {url}: {e}")
            return None

    def crawl_recursive(self):
        visited = set()
        queue = Queue()
        queue.put(self.start_url)
        results = []

        while not queue.empty() and len(visited) < self.crawl_limit:
            url = queue.get()
            if url in visited or not can_crawl(url):
                continue
            visited.add(url)

            page_data = self.crawl_page(url)
            if page_data:
                results.append(page_data)

                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "html.parser")
                    for link in soup.find_all("a", href=True):
                        href = clean_url(link["href"], url)
                        if is_same_domain(href, self.start_url) and href not in visited:
                            queue.put(href)
                except requests.RequestException as e:
                    print(f"Error fetching links from {url}: {e}")

        return results


def crawl_recursive(start_url=START_URL):
    """Legacy function for compatibility."""
    crawler = Crawler(start_url)
    return crawler.crawl_recursive()


if __name__ == "__main__":
    crawler = Crawler()
    pages = crawler.crawl_recursive()
    for page in pages:
        print(f"Crawled: {page['url']}, Title: {page['title']}")
