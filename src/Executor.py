import requests
import bs4
import pandas as pd
from config import constantes as const

class Executor:

    scraper = None
    extractor = None
    analyzer = None

    def __init__(self, scraper, extractor, analyzer):
        super().__init__()
        self.scraper = scraper
        self.extractor = extractor
        self.analyzer = analyzer
    
    def lancerTraitement(self, url):
        if url == "http://phonesdata.com/fr/smartphones/":
            htmlComplet = self.scraper.scrapUrl(url)
            marquesUrlsList = map(self.traitementHtmlPrimaire, htmlComplet.find_all("p", {"class": "list-items"}))
            marquesUrlsList = [i for i in marquesUrlsList if i]

            marqueAnneesUrlList = map(self.traitementMarquesUrls, marquesUrlsList)
            marqueAnneesUrlList = [y for x in marqueAnneesUrlList for y in x]

            anneeTelephoneList = map(self.traitementAnneesUrls, marqueAnneesUrlList)
            anneeTelephoneList = [y for x in anneeTelephoneList for y in x]
            
            dfList = map(self.traitementTelephoneInfo, anneeTelephoneList)
            allData = pd.concat(list(dfList))
            
            return allData.set_index("Nom")  
        elif url == "https://www.phonearena.com/phones/benchmarks":
            htmlComplet = self.scraper.scrapUrl(url)
            benchmarksHtml = htmlComplet.find_all("div", {"class": "widget-benchmark"})
            performanceDF, DureeBatterieDF, ChargementBatterieDF = self.extractor.extractBenchmarkDF(benchmarksHtml)
            tmpDF = pd.merge(DureeBatterieDF, ChargementBatterieDF, on="Nom", how="outer")
            result = pd.merge(performanceDF, tmpDF, on="Nom", how="outer")
            
            return result.set_index("Nom")
    

    # http://phonesdata.com/fr/smartphones

    def traitementHtmlPrimaire(self, html):
        return self.extractor.extractUrlParMarque(html)

    def traitementMarquesUrls(self, marqueUrl):
        htmlMarque = self.scraper.scrapUrl(marqueUrl)
        return self.extractor.extractUrlParAnneeMarque(htmlMarque, marqueUrl)

    def traitementAnneesUrls(self, marqueAnneeUrl):
        htmlTelephoneAnnee = self.scraper.scrapUrl(marqueAnneeUrl)
        return self.extractor.extractUrlTelephoneParAnnee(htmlTelephoneAnnee)
    
    def traitementTelephoneInfo(self, urlTelephone):
        htmlTelephone = self.scraper.scrapUrl(urlTelephone)
        return self.extractor.extractTelephoneInfo(htmlTelephone)
    

    # http://phonesdata.com/fr/smartphones