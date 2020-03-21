from config import constantes as const
from src.Scraper import Scraper
import pandas as pd

class Extractor:

    def __init__(self):
        super().__init__()
    
    def extractMarque(self, marqueUrl):
        marqueUrlSplit = marqueUrl.split("/")
        marque = marqueUrlSplit[len(marqueUrlSplit)-2]
        return marque
    
    def extractNomTelephone(self, html):
        divProductPage = html.find("div", {"class": "product-page"})
        h1NomTelephone = divProductPage.find("h1").text
        nomTelephone = h1NomTelephone[:h1NomTelephone.index(" Fiche")]
        return nomTelephone
    
    def extraireInfo(self, allElement):
        key = None
        resultat = {}
        for td in allElement:
            try:
                if td['class']:
                    key = " ".join(td.text.strip().split())
            except KeyError:
                if key == None:
                    key = "Autres"
                resultat[key] = " ".join(td.text.strip().split())
        return resultat

    def extractInfoFromDivId(self, html, divId):
        table = html.find("table", {"id": divId})
        infoId = self.extraireInfo(table.find_all("td"))
        return infoId

    def extractUrlParMarque(self, html):
        marqueUrlList = []
        for p in html.find_all("p", {"class": "list-items"}):
            marqueUrl = p.find("a").get("href")
            if self.extractMarque(marqueUrl) in const.marquesVise:
                marqueUrlList.append(marqueUrl)
        return marqueUrlList
    
    def extractUrlParAnneeMarque(self, html, marqueUrl):
        anneeMarqueUrlList = []
        div = html.find("div", {"class": "row product-page"})
        for a in div.find_all("a"):
            urlAnneeMarque = a.get("href")
            if (urlAnneeMarque.startswith(marqueUrl + "#2") or urlAnneeMarque.startswith(marqueUrl + "2")) and len(urlAnneeMarque.replace(marqueUrl, "")) == 5:
                if urlAnneeMarque not in anneeMarqueUrlList:
                    anneeMarqueUrlList.append(urlAnneeMarque)
        return anneeMarqueUrlList
    
    def extractTelephoneInfo(self, html, scraper, allData):
        for p in html.find_all("p", {"class": "list-items"}):
            urlTelephone = p.find("a").get("href")
            infosTelephone = {}
            htmlTelephone = scraper.scrapUrl(urlTelephone)
            infosTelephone["Nom"] = self.extractNomTelephone(htmlTelephone)
            infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "displaytec"))
            infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "cameratec"))
            infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "cputec"))
            infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "commontec"))
            infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "connetctec"))
            infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "audiotec"))
            infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "otherstec"))
            infosDF = pd.DataFrame(infosTelephone, index=[0])
            allData = pd.concat([allData, infosDF])
        return allData


