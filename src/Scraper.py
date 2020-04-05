import requests
import bs4
import logging
import json
from config import config as cnf

class Scraper:

    headers = None

    def __init__(self):
        super().__init__()
        self.headers = json.loads(cnf.config["DEFAULT"]["headers"])
    
    def scrapUrl(self, url):
        logging.info("Scrapping de l'URL : " + str(url))
        html = requests.get(url, headers=self.headers)
        soup = bs4.BeautifulSoup(html.text, features="html.parser")
        return soup