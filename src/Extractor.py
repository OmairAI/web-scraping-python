import pandas as pd
import json
from config import config as cnf

class Extractor:

    marquesVise = None

    def __init__(self):
        super().__init__()
        self.marquesVise = json.loads(cnf.config["DEFAULT"]["marquesVise"])
    
    def extractMarque(self, marqueUrl):
        marqueUrlSplit = marqueUrl.split("/")
        marque = marqueUrlSplit[len(marqueUrlSplit)-2]
        return marque
    
    def extractNomTelephone(self, html):
        divProductPage = html.find("div", {"class": "product-page"})
        h1NomTelephone = divProductPage.find("h1").text
        nomTelephone = h1NomTelephone[:h1NomTelephone.index(" Fiche")]
        nomTelephone = " ".join(nomTelephone.strip().split())
        cnf.logger.debug("Nom téléphone récupérée : {0}".format(str(nomTelephone)))
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
            if key == "Prix approximatif" and " EUR" not in " ".join(td.text.strip().split()):
                resultat[key] = None
            else:
                resultat[key] = " ".join(td.text.strip().split())
        return resultat

    def extractInfoFromDivId(self, html, divId):
        table = html.find("table", {"id": divId})
        infoId = self.extraireInfo(table.find_all("td"))
        cnf.logger.debug("Informations récupérées depuis le div avec l'id {0} : {1}".format(str(divId), str(infoId)))
        return infoId

    def extractUrlParMarque(self, p):
        marqueUrl = p.find("a").get("href")
        marque = self.extractMarque(marqueUrl)
        cnf.logger.debug("Marque récupérée : {0}".format(str(marque)))
        if marque in self.marquesVise:
            cnf.logger.debug("URL marque téléphone récupérée : {0}".format(str(marqueUrl)))
            return marqueUrl
        else:
            cnf.logger.debug("{0} n'est pas dans les marques visées : ne sera pas traitée".format(str(marque)))
    
    def extractUrlParAnneeMarque(self, html, marqueUrl):
        anneeMarqueUrlList = []
        div = html.find("div", {"class": "row product-page"})
        for a in div.find_all("a"):
            urlAnneeMarque = a.get("href")
            if (urlAnneeMarque.startswith(marqueUrl + "#2") or urlAnneeMarque.startswith(marqueUrl + "2")) and len(urlAnneeMarque.replace(marqueUrl, "")) == 5:
                if urlAnneeMarque not in anneeMarqueUrlList:
                    anneeMarqueUrlList.append(urlAnneeMarque)
                    cnf.logger.debug("URL marque - année téléphone récupérée : {0}".format(str(urlAnneeMarque)))
        return anneeMarqueUrlList

    def extractUrlTelephoneParAnnee(self, htmlTelephoneAnnee):
        urlTelephone = map(self.getTelephoneHref, htmlTelephoneAnnee.find_all("p", {"class": "list-items"}))
        return urlTelephone
    
    def getTelephoneHref(self, item):
        return item.find("a").get("href")
    
    def extractTelephoneInfo(self, htmlTelephone):
        infosTelephone = {}
        infosTelephone["Nom"] = self.extractNomTelephone(htmlTelephone)
        infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "displaytec"))
        infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "cameratec"))
        infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "cputec"))
        infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "commontec"))
        infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "connetctec"))
        infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "audiotec"))
        infosTelephone.update(self.extractInfoFromDivId(htmlTelephone, "otherstec"))
        infosDF = pd.DataFrame(infosTelephone, index=[infosTelephone["Nom"]])
        return infosDF
    
    
    def extractBenchmarkLegende(self, benchmarkHtml):
        legendeHtml = benchmarkHtml.find(class_="sort_container")
        dictLegende = {}
        try:
            AllH3Html = legendeHtml.find_all("h3", {"class": "tooltip"})
            for h3Html in AllH3Html:
                libelleLegende = " ".join(h3Html.text.strip().replace("\n", " - ").split())
                blockHtml = h3Html.find("span", {"class": "block"})
                dictLegende[blockHtml.get("style")] = libelleLegende
        except:
            pass
        cnf.logger.debug("Légende récupérée : {0}".format(str(dictLegende)))
        return dictLegende

    def concatDataframe(self, htmlBgColor, performanceDF, DureeBatterieDF, ChargementBatterieDF, benchmarkTelephoneDF, cpt):
        if "blue" not in htmlBgColor["class"]:
            performanceDF = pd.concat([performanceDF, benchmarkTelephoneDF])
        elif "blue" in htmlBgColor["class"] and cpt == 8:
            DureeBatterieDF = pd.concat([DureeBatterieDF, benchmarkTelephoneDF])
        elif "blue" in htmlBgColor["class"] and cpt == 9:
            ChargementBatterieDF = pd.concat([ChargementBatterieDF, benchmarkTelephoneDF])
        return performanceDF, DureeBatterieDF, ChargementBatterieDF

    def extractBenchmark(self, benchmarkHtml, dictLegende, cpt, performanceDF, DureeBatterieDF, ChargementBatterieDF):
        rowsBenchmarkHtml = benchmarkHtml.find_all("tr", {"class": "row clear"})
        for row in rowsBenchmarkHtml:
            benchmarkTelephone = {}
            benchmarkTelephoneDF = pd.DataFrame()
            nomTelephone = row.find("div", {"class": "name"})
            if nomTelephone.text.split()[0].lower() in self.marquesVise:
                benchmarkTelephone["Nom"] = nomTelephone.text.strip()
                scores = row.find_all("div", {"class": "score"})
                for score in scores:
                    htmlBgColor = score.find("span", {"class": "block"})
                    benchmarkTelephone = self.extractBenchmarkScore(htmlBgColor, score, benchmarkTelephone, dictLegende)
                    benchmarkTelephoneDFUnique = pd.DataFrame(benchmarkTelephone, index=[benchmarkTelephone["Nom"]]) 
                    benchmarkTelephoneDF = pd.concat([benchmarkTelephoneDF, benchmarkTelephoneDFUnique], axis=1)
                    benchmarkTelephoneDF = benchmarkTelephoneDF.loc[:,~benchmarkTelephoneDF.columns.duplicated()]
                performanceDF, DureeBatterieDF, ChargementBatterieDF = self.concatDataframe(htmlBgColor, performanceDF, DureeBatterieDF, ChargementBatterieDF, benchmarkTelephoneDF, cpt)
        return performanceDF, DureeBatterieDF, ChargementBatterieDF

    def extractBenchmarkScore(self, htmlBgColor, htmlScore, benchmarkTelephone, dictLegende):
        benchmarkScore = htmlScore.find("span", {"class": "stext"}).text.strip()
        if "blue" not in htmlBgColor["class"]:
            bgColor = htmlBgColor.get("style").split(";")[1].strip()
            benchmarkTelephone[dictLegende[bgColor]] = benchmarkScore
        elif "blue" in htmlBgColor["class"] and "h" in benchmarkScore:
            try:
                benchmarkScore = benchmarkScore[:benchmarkScore.index(" min")]
            except:
                benchmarkScore = benchmarkScore[:benchmarkScore.index("(")]
            benchmarkScore = benchmarkScore.split("h ")
            try:
                benchmarkScore = int(benchmarkScore[0]) * 60 + int(benchmarkScore[1])
            except:
                benchmarkScore = int(benchmarkScore[0]) * 60
            benchmarkTelephone["Durée batterie"] = benchmarkScore
        elif "blue" in htmlBgColor["class"]:
            benchmarkTelephone["Temps chargement"] = benchmarkScore
        cnf.logger.debug("Benchmark téléphone récupérée : {0}".format(str(benchmarkTelephone)))
        return benchmarkTelephone
    
    def extractBenchmarkDF(self, benchmarksHtml):
        performanceDF = pd.DataFrame()
        DureeBatterieDF = pd.DataFrame()
        ChargementBatterieDF = pd.DataFrame()
        cpt = 0
        indexVoulu = [5, 8, 9]
        for benchmarkHtml in benchmarksHtml:
            if cpt in indexVoulu:
                dictLegende = self.extractBenchmarkLegende(benchmarkHtml)
                performanceDF, DureeBatterieDF, ChargementBatterieDF = self.extractBenchmark(benchmarkHtml, dictLegende, cpt, performanceDF, DureeBatterieDF, ChargementBatterieDF)
            cpt += 1
        return performanceDF, DureeBatterieDF, ChargementBatterieDF