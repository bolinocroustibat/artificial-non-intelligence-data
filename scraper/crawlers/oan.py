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


class OANCrawler(CommentsCrawler):

    # The name of the crawler
    name = "oan"

    # The URL format that is allowed to be considered as valid articles to parse
    allowed_urls = [
        "www.oann.com/category/newsroom/",
    ]

    # The URLs to start with
    start_urls = [
        # "https://www.oann.com/category/newsroom/",
        "https://www.oann.com/cbp-prevents-chinese-fishing-company-from-importing-goods-into-u-s-due-to-widespread-human-rights-abuses/",
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
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "disqus_thread")))
    
        except TimeoutException:
            self.error("Couldn't find comments section within 3sec, closing.")
            driver.close()

        else:

            try:
                self.debug("Scrolling to the comments section to force comments loading...")
                driver.find_element_by_id("disqus_thread") # scroll the the right section
            except:
                self.debug("Couldn't scroll to the comments section, closing.")
                driver.close()
            else:
                self.debug("Found Disqus section. Get comments...")
                wait = WebDriverWait(driver, delay)
                element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".post-message"))) # Wait until the element appears
