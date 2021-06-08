import requests
from bs4 import BeautifulSoup

from .blueprint import CommentsCrawler


class ValeursactuellesCrawler(CommentsCrawler):

    # The name of the crawler
    name = "valeursactuelles"

    # The urls that are allowed as articles
    allowed_urls = [
        "www.valeursactuelles.com/faits-divers/",
        "www.valeursactuelles.com/societe/",
        "www.valeursactuelles.com/politique/",
        "www.valeursactuelles.com/editos/",
        "www.valeursactuelles.com/monde/",
        "www.valeursactuelles.com/clubvaleurs/politique/",
        # "www.valeursactuelles.com/clubvaleurs/lincorrect/"
    ]

    # The URLs to start with
    start_urls = [
        "https://www.valeursactuelles.com/",
        "https://www.valeursactuelles.com/faits-divers",
        "https://www.valeursactuelles.com/societe",
        "https://www.valeursactuelles.com/politique",
        "https://www.valeursactuelles.com/editos",
        "https://www.valeursactuelles.com/clubvaleurs",
        "https://www.valeursactuelles.com/monde",
    ]

    def parse_comments(self, url: str, article_id: int) -> None:
        try:
            html = requests.get(url, headers=self.HEADERS).content
        except Exception as e:
            self.error(f"Request error: {str(e)}")
        else:
            soup = BeautifulSoup(html, "html.parser")
            for comment_soup in soup.find_all("div", id="comments"):
            # for comment_soup in soup.find_all("article", class_="comment-body"): 
                author_soup = comment_soup.find("div", class_="comment-author")
                message_soup = comment_soup.find("div", class_="comment__content")
                try:
                    if "a été supprimé car il ne respecte pas notre" not in message_soup.string:
                        self.record_comment_in_db(article_id, author_soup.string, message_soup.string)
                except Exception as e:
                    self.error(f"Couldn't launch the record comment function: {str(e)}")
