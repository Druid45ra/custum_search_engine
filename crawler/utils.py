from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import re


def is_valid_url(url):
    """Check if URL is valid."""
    try:
        result = requests.head(url, allow_redirects=True, timeout=5)
        return result.status_code == 200
    except requests.RequestException:
        return False


def clean_url(url, base_url):
    """Convert relative URLs to absolute and normalize."""
    return urljoin(base_url, url.strip())


def is_same_domain(url, base_url):
    """Check if URL belongs to the same domain."""
    base_domain = urlparse(base_url).netloc
    url_domain = urlparse(url).netloc
    return base_domain == url_domain


def parse_html(content):
    """Extract title and clean text from HTML."""
    soup = BeautifulSoup(content, "html.parser")
    title = soup.title.string if soup.title else ""
    text = " ".join(soup.get_text().split())
    return title, text


def can_crawl(url):
    """Check if URL is allowed by robots.txt."""
    robots_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch("*", url)
    except:
        return True  # Allow if robots.txt is inaccessible
