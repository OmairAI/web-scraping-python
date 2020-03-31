import json
import pandas as pd
import configparser
import matplotlib.pyplot as plt

from src.Executor import Executor
from src.Scraper import Scraper
from src.Extractor import Extractor
from src.Analyze import Analyze
from config import constantes as const

allDataList = []
config = configparser.ConfigParser()

def getFichierJSON():
    with open(config["DEFAULT"]["fichierJson"]) as fichierJSON:
        return json.load(fichierJSON)

def main():
    scraper = Scraper()
    extractor = Extractor()
    analyzer = Analyze()
    executor = Executor(scraper, extractor, analyzer)

    urls = getFichierJSON()
    for url in urls["url"]:
        allData = executor.lancerTraitement(url)
        allDataList.append(allData)
        allData.to_csv("/Users/omair/Desktop/M1/ProgAv2/output/" + url.replace("/", "").replace(":", "") + ".csv", sep="\t")

    finalDF = pd.merge(allDataList[0], allDataList[1], on="Nom", how="outer")

    analyseDF = finalDF[["Nom", "Temps chargement"]]
    analyseDF[["Temps chargement"]] = analyseDF[["Temps chargement"]].astype(float)
    fig = analyseDF.dropna().plot(x="Nom", kind="barh")
    plt.show()
    
if __name__ == "__main__":
    config.read("/Users/omair/Desktop/M1/ProgAv2/Projet/config/config.ini")
    main()