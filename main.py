import json
import pandas as pd

from src.Scraper import Scraper
from src.Extractor import Extractor
from src.Analyze import Analyze
from config import constantes as const

allData = pd.DataFrame()

def getFichierJSON():
    with open(const.pathFichierJSON) as fichierJSON:
        return json.load(fichierJSON)

def main():
    scraper = Scraper()
    extractor = Extractor()
    analyzer = Analyze()

    urls = getFichierJSON()
    for url in urls["url"]:
        htmlComplet = scraper.scrapUrl(url)
        marquesUrls = extractor.extractUrlParMarque(htmlComplet)
    
    marqueAnneesUrlDict = {}
    for marqueUrl in marquesUrls:
        htmlMarque = scraper.scrapUrl(marqueUrl)
        marqueAnneesUrlDict[extractor.extractMarque(marqueUrl)] = extractor.extractUrlParAnneeMarque(htmlMarque, marqueUrl)
    
    allData = pd.DataFrame()
    for marque, marqueAnneeUrlList in marqueAnneesUrlDict.items():
        for urlMarqueAnnee in marqueAnneeUrlList:
            htmlMarqueAnnee = scraper.scrapUrl(urlMarqueAnnee)
            allData = extractor.extractTelephoneInfo(htmlMarqueAnnee, scraper, allData)
    
    print(allData)
    allData.to_csv("/Users/omair/Desktop/M1/ProgAv2/output/dataframenlsjdnljd.csv", sep="\t")

if __name__ == "__main__":
    main()