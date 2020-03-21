import requests
import bs4
from config import constantes as const

class Scraper:

    def __init__(self):
        super().__init__()
    
    def scrapUrl(self, url):
        html = requests.get(url, headers=const.headers)
        soup = bs4.BeautifulSoup(html.text, features="html.parser")
        return soup