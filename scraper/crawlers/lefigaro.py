import requests
from bs4 import BeautifulSoup

from .blueprint import CommentsCrawler


class FigaroCrawler(CommentsCrawler):

    # The name of the crawler
    name = "figaro"

    # The urls that are allowed as articles
    allowed_urls = [
        "www.lefigaro.fr/flash-actu",
        "www.lefigaro.fr/societe",
        "www.lefigaro.fr/politique",
        "www.lefigaro.fr/vox/politique",
        "www.lefigaro.fr/vox/societe",
        "www.lefigaro.fr/actualite-france"
    ]

    # The URLs to start with
    start_urls = [
        "https://www.lefigaro.fr/",
        "https://www.lefigaro.fr/actualite-france"
        "https://www.lefigaro.fr/flash-actu/",
        "https://www.lefigaro.fr/politique/le-scan",
        "https://www.lefigaro.fr/politique/le-scan/citations",
        "https://www.lefigaro.fr/vox",
        "https://www.lefigaro.fr/vox/politique",
        "https://www.lefigaro.fr/vox/societe",
        "https://www.lefigaro.fr/",
        "https://www.lefigaro.fr/flash-actu/",
        "https://www.lefigaro.fr/politique/le-scan",
        "https://www.lefigaro.fr/politique/le-scan/citations",
        "https://www.lefigaro.fr/vox",
        "https://www.lefigaro.fr/vox/politique",
        "https://www.lefigaro.fr/vox/societe"
    ]

    def parse_comments(self, url: str, article_id: int) -> None:
        try:
            html = requests.get(url, headers=self.HEADERS).content
        except Exception as e:
            self.error(f"Request error: {str(e)}")
        else:
            soup = BeautifulSoup(html, "html.parser")
            for comment_soup in soup.find_all("li", class_="fig-comments__item"):
                author: str = comment_soup.find("p", class_="fig-comment__username").get_text()
                message: str = comment_soup.find("p", class_="fig-comment__text").get_text()
                self.record_comment_in_db(article_id, author, message)
