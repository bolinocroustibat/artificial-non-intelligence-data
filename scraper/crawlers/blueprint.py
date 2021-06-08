from peewee import IntegrityError
import typer
import re
import requests
from bs4 import BeautifulSoup

from models import Website, Article, Comment


class CommentsCrawler():

    HEADERS: str = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    urls_to_parse: list = []

    def debug(self, message: any):
        typer.secho(
            str(message),
            fg=typer.colors.CYAN,
        )

    def info(self, message: any):
        typer.secho(
            str(message),
            fg=typer.colors.BLUE,
        )

    def success(self, message: any):
        typer.secho(
            f"\n{str(message)}",
            fg=typer.colors.GREEN,
        )

    def error(self, message: any):
        typer.secho(
            f"\n{str(message)}",
            fg=typer.colors.RED,
        )

    def extract_links(self, url: str) -> list:
        # Extract links from url
        html = requests.get(url, headers=self.HEADERS).content
        soup = BeautifulSoup(html, "html.parser")
        links_soup = soup.findAll('a', href=re.compile(r'\b(?:{})\b'.format('|'.join(self.allowed_urls)))) # https://stackoverflow.com/questions/6750240/how-to-do-re-compile-with-a-list-in-python
        # self.debug(str(links_soup))
        return [l['href'] for l in links_soup]


    def start(self):
        """
        Method which starts the requests by visiting all URLs specified in start_urls
        """
        self.website = Website.get(Website.short_name == self.name)

        old_articles_nb: int = Article.select().count()
        old_comments_nb: int = Comment.select().count()

        for url in self.start_urls:
            self.parse_article(url=url, url_from="")
            for link in self.extract_links(url):
                # Go through all the found links
                self.parse_article(url=link, url_from=url)

        # Final output for this start URL
        new_articles_nb: int = Article.select().count()
        new_comments_nb: int = Comment.select().count()
        self.success(
            f"\nScraping completed!\nThere were {old_articles_nb} articles in the DB before, {new_articles_nb} now.\nThere were {old_comments_nb} comments in the DB before, {new_comments_nb} now."
        )


    def parse_article(self, url: str, url_from: str):
        """
        Try to save the article in the DB, and launch the comments parsing
        """
        self.debug(f"Parsing article {url}...")
        article = Article(url=url, url_from=url_from)
        article.website = self.website
        article_id = None
        try:
            article.save()
            try:
                article_id = article.id
            except Exception as e:
                self.error(e)
            else:
                self.success("New article saved in DB!")
        except IntegrityError as e:
            if "UNIQUE constraint" in e.args[0]:
                article_id = Article.get(url=url).id
                self.info(f'Article already exists in DB as id {article_id}, skipping saving it in DB')
        except Exception as e:
            self.error(f"Unknown error while saving article in DB: {e}")
        self.parse_comments(url=url, article_id=article_id) # pass the article ID to the comment parser so we can associate the comment with the article in the DB


    def record_comment_in_db(self, article_id: int, author: str, message: str) -> None:
        comment = Comment(author=author, message=message)
        try:
            comment.article = Article.get(id=article_id)
        except Exception as e:
            self.error("	Couldn't associate the comment with an article.")
        try:
            comment.save()
        except IntegrityError as e:
            if "UNIQUE constraint" in e.args[0]:
                self.info("	Comment already exists in DB, skipping.")
        except Exception as e:
            self.error(f"	Error while saving comment: {e}")
        else:
            self.success(f"	New comment saved in DB!\n	AUTHOR: {author}\n	MESSAGE: {message[0:40]}...")
