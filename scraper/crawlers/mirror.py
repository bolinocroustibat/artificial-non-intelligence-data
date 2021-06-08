import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_binary

from .blueprint import CommentsCrawler


class MirrorCrawler(CommentsCrawler):

    # The name of the crawler
    name = "mirror"

    # The URL format that is allowed to be considered as valid articles to parse
    allowed_urls = [
        "www.mirror.co.uk/news/politics",
        "www.mirror.co.uk/news/uk-news"
    ]

    # The URLs to start with
    start_urls = [
        "https://www.mirror.co.uk/news/politics",
        "https://www.mirror.co.uk/news/politics/carrie-symonds-married-boris-johnson-24217600",
        "https://www.mirror.co.uk/news/uk-news/thousands-call-prince-harry-give-24217252"
    ]

    def parse_comments(self, url: str, article_id: int) -> None:

        self.debug(f"Parsing comments from {url}...")

        # Chrome with UI
        driver = webdriver.Chrome()

        # # Headless Chrome (without UI)
        # options = Options()
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(options=options)

        # driver.set_page_load_timeout(5)
        driver.get(url)
        
        delay: int = 3 # seconds

        try:
            self.debug("Locating comments section...")
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "comments-wrapper")))
    
        except TimeoutException:
            self.error("Couldn't find a comment wrapper section within 3sec, closing.")
            driver.close()

        else:

            try:
                self.debug("Scrolling to the comments section to force comments loading...")
                driver.find_element_by_id("comments-wrapper") # scroll the the right section
            except:
                self.debug("Couldn't scroll to the comment wrapper, closing.")
                driver.close()
            else:
                self.debug("Wait for the comments to load...")
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".vf-content-text"))) # Wait until the element appears
                try:
                    comment = driver.find_elements_by_class_name("vf-content-text")
                    self.debug(comment.text)
                except:
                    self.error("Found the comment wrapper, but couldn't find comments inside.")
                    driver.close()
