from urllib.parse import urlparse


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_robots_parser(url):
    # TODO: Poți integra robotparser aici, dacă vrei respect strict robots.txt
    pass
