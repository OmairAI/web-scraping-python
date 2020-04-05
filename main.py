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

    if (args["save"] == "True"):
        finalDF = getDataDF(scrapData, (executor, getFichierJSON()))
    elif args["read"] == "True":
        finalDF = getDataDF(readFromCSV, (cnf.config["CSV"]["pathRead"], "\t"))
        
    analyseData(analyzer, finalDF, args["analyse"])

def getDataDF(operation, args):
    cnf.logger.info("Début de l'opération : {0}".format(operation.__name__))
    return operation(*args)

def saveToCSV(df, path, sep):
    df.to_csv(path, sep=sep)

def readFromCSV(path, sep):
    return pd.read_csv(path, sep=sep)

def mergeListDF(listDF, colonne, how):
    tmpDF = pd.merge(listDF[0], listDF[1], on=colonne, how=how)
    tmpDF[colonne] = tmpDF.index
    return tmpDF

def analyseData(analyzer, finalDF, analyse):
    if analyse == 'True':
        analyzer.genereGraph(analyzer.moyennePrixParAnGraph, finalDF).show()
        analyzer.genereGraph(analyzer.moyenneDureeBatterieParAnGraph, finalDF).show()
        analyzer.genereGraph(analyzer.moyenneTempsChargementParAnGraph, finalDF).show()
        analyzer.genereGraph(analyzer.repartitionPrixSmartphoneGraph, finalDF).show()
        analyzer.genereGraph(analyzer.repartitionOSGraph, finalDF).show()

def scrapData(executor, urls):
    allDataList = list(map(traitementUrl, urls["url"], repeat(executor)))
    finalDF = mergeListDF(allDataList, "Nom", "outer")
    saveToCSV(finalDF, cnf.config["CSV"]["pathSave"], "\t")
    return finalDF

    
if __name__ == "__main__":
    args = cnf.parseArgs()
    config = cnf.initialiseConfig(args["config"])
    logger = cnf.initialiseLog()
    
    cnf.logger.info("Début du traitement")
    main(args)
    cnf.logger.info("Fin du traitement")