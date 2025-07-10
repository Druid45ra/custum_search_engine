from crawler.crawler import Crawler
from indexer.indexer import Indexer
from config.settings import START_URL


def main():
    crawler = Crawler(start_url=START_URL)
    pages = crawler.crawl_recursive()
    print(f"Total pages crawled: {len(pages)}")
    for page in pages:
        print(f"Crawled: {page['url']}, Title: {page['title']}")

    # Index the crawled pages
    indexer = Indexer()
    indexer.index_documents(pages)
    print(f"Indexed {len(pages)} pages to Elasticsearch")


if __name__ == "__main__":
    main()
