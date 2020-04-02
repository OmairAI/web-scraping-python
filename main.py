import json
import pandas as pd
import configparser
import matplotlib.pyplot as plt
from itertools import repeat
import plotly.express as px
import logging

from src.Executor import Executor
from src.Scraper import Scraper
from src.Extractor import Extractor
from src.Analyze import Analyze
from config import config as cnf

allDataList = []

def getFichierJSON():
    with open(cnf.config["DEFAULT"]["fichierJson"]) as fichierJSON:
        return json.load(fichierJSON)

def traitementUrl(url, executor):
    return executor.lancerTraitement(url)

def main(args):
    scraper = Scraper()
    extractor = Extractor()
    analyzer = Analyze()
    executor = Executor(scraper, extractor, analyzer)

    finalDF = scrapData(args["save"], executor)
    finalDF = readFromCSV("/Users/omair/Desktop/M1/ProgAv2/output/finalDF.csv", "\t", args["read"])
    analyseData(analyzer, finalDF, args["analyse"])


def saveToCSV(df, path, sep):
    df.to_csv(path, sep=sep)

def readFromCSV(path, sep, read):
    if read == 'True':
        return pd.read_csv(path, sep=sep)

def mergeListDF(listDF, colonne, how):
    tmpDF = pd.merge(listDF[0], listDF[1], on=colonne, how=how)
    tmpDF[colonne] = tmpDF.index
    return tmpDF

def analyseData(analyzer, finalDF, analyse):
    if analyse == 'True':
        analyzer.moyennePrixParAnGraph(finalDF).show()
        analyzer.moyenneDureeBatterieParAnGraph(finalDF).show()
        analyzer.moyenneTempsChargementParAnGraph(finalDF).show()
        analyzer.repartitionPrixSmartphoneGraph(finalDF).show()
        analyzer.repartitionOSGraph(finalDF).show()

def scrapData(scrap, executor):
    if scrap == 'True':
        urls = getFichierJSON()
        allDataList = list(map(traitementUrl, urls["url"], repeat(executor)))
        finalDF = mergeListDF(allDataList, "Nom", "outer")
        saveToCSV(finalDF, "/Users/omair/Desktop/M1/ProgAv2/output/finalDF.csv", "\t")
        return finalDF

    
if __name__ == "__main__":
    args = cnf.parseArgs()
    config = cnf.initialiseConfig(args["config"])
    logger = cnf.initialiseLog()
    
    cnf.logger.info("Début du traitement")
    main(args)