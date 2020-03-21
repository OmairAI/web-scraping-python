import urllib.request
import requests
import bs4
import json
import pandas as pd

import Scraper
import Extractor
import Analyze

allData = pd.DataFrame()

marquesVise = ["apple", "samsung", "huawei", "oneplus", "oppo", "google", "htc", "lg", "sony", "xiaomi"]

url = "http://phonesdata.com/fr/smartphones/"
#url = "http://phonesdata.com/fr/smartphones/apple/iphone-11-pro-5458276/"

html = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(html.text, features="html.parser")

# Fonction récupération tableau technique
def extraireInfo(allElement):
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


marqueUrlList = []
for p in soup.find_all("p", {"class": "list-items"}):
    marqueUrlList.append(p.find("a").get("href"))

urlParMarque = {}

for marqueUrl in marqueUrlList:
    marqueUrlSplit = marqueUrl.split("/")
    marque = marqueUrlSplit[len(marqueUrlSplit)-2]
    if marque in marquesVise:
        html = requests.get(marqueUrl, headers=headers)
        soup = bs4.BeautifulSoup(html.text, features="html.parser")
        anneeUrlList = []
        telephoneParMarqueUrl = []
        div = soup.find("div", {"class": "row product-page"})
        for a in div.find_all("a"):
            hrefMarqueAnnee = a.get("href")
            if (hrefMarqueAnnee.startswith(marqueUrl + "#2") or hrefMarqueAnnee.startswith(marqueUrl + "2")) and len(hrefMarqueAnnee.replace(marqueUrl, "")) == 5:
                if hrefMarqueAnnee not in anneeUrlList:
                    anneeUrlList.append(hrefMarqueAnnee)
                    html = requests.get(hrefMarqueAnnee, headers=headers)
                    soup = bs4.BeautifulSoup(html.text, features="html.parser")
                    for p in soup.find_all("p", {"class": "list-items"}):
                        telephoneParMarqueUrl.append(p.find("a").get("href"))

                        infosTelephone = {}
                        html = requests.get(p.find("a").get("href"), headers=headers)
                        soup = bs4.BeautifulSoup(html.text, features="html.parser")

                        # Nom du téléphone
                        divProductPage = soup.find("div", {"class": "product-page"})
                        h1NomTelephone = divProductPage.find("h1").text
                        nomTelephone = h1NomTelephone[:h1NomTelephone.index(" Fiche")]
                        print(nomTelephone)
                        infosTelephone["Nom"] = nomTelephone

                        # Fiche technique
                        tableFicheTechnique = soup.find("table", {"id": "displaytec"})
                        ficheTechnique = extraireInfo(tableFicheTechnique.find_all("td"))
                        infosTelephone.update(ficheTechnique)

                        # Camera
                        tableCamera = soup.find("table", {"id": "cameratec"})
                        camera = extraireInfo(tableCamera.find_all("td"))
                        infosTelephone.update(camera)

                        # Performance
                        tablePerformance = soup.find("table", {"id": "cputec"})
                        performance = extraireInfo(tablePerformance.find_all("td"))
                        infosTelephone.update(performance)

                        # Caracteristiques
                        tableCaracteristiques = soup.find("table", {"id": "commontec"})
                        caracteristiques = extraireInfo(tableCaracteristiques.find_all("td"))
                        infosTelephone.update(caracteristiques)

                        # Connectivité
                        tableConnectivite = soup.find("table", {"id": "connetctec"})
                        connectivite = extraireInfo(tableConnectivite.find_all("td"))
                        infosTelephone.update(connectivite)

                        # Audio
                        tableAudio = soup.find("table", {"id": "audiotec"})
                        audio = extraireInfo(tableAudio.find_all("td"))
                        infosTelephone.update(audio)

                        # Autres
                        tableAutres = soup.find("table", {"id": "otherstec"})
                        autres = extraireInfo(tableAutres.find_all("td"))
                        infosTelephone.update(autres)

                        infosDF = pd.DataFrame(infosTelephone, index=[0])

                        allData = pd.concat([allData, infosDF])

        
        print(allData)
        print("-------------------")


allData.to_csv("/Users/omair/Desktop/M1/ProgAv2/output/dataframe.csv", sep="\t")