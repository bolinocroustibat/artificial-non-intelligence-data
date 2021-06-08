import typer

from crawlers.lefigaro import FigaroCrawler
from crawlers.mirror import MirrorCrawler
from crawlers.oan import OANCrawler
from crawlers.valeursactuelles import ValeursactuellesCrawler

CRAWLERS: dict = {
    "lefigaro": FigaroCrawler,
    "mirror": MirrorCrawler,
    "oan": OANCrawler,
    "valeursactuelles": ValeursactuellesCrawler,
}

def crawl(crawler_name: str):
    crawler = CRAWLERS[crawler_name]()
    crawler.start()

if __name__ == "__main__":
    typer.run(crawl)
