from crawler.crawler import Crawler


def test_crawler_basic():
    crawler = Crawler("https://example.com", max_depth=1)
    assert crawler.start_url == "https://example.com"
