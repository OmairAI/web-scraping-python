import requests
import bs4
import logging
from config import constantes as const

class Scraper:

    def __init__(self):
        super().__init__()
    
    def scrapUrl(self, url):
        logging.info("Scrapping de l'URL : " + str(url))
        html = requests.get(url, headers=const.headers)
        soup = bs4.BeautifulSoup(html.text, features="html.parser")
        return soup