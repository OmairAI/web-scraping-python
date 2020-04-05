import unittest
import pandas as pd
from src.Executor import Executor
from src.Scraper import Scraper
from src.Extractor import Extractor
from src.Analyze import Analyze

class MainTest(unittest.TestCase):
    
    def test_extractMarque(self):
        # GIVEN : préparer les données du test
        extractor = Extractor()
        url = "https://phonesdata.com/fr/smartphones/apple/"
        resultatAttendu = "apple"
        # WHEN : exécuter la fonction testée
        resultatObtenu = extractor.extractMarque(url)
        # THEN : vérifier les résultats
        self.assertEqual(resultatObtenu, resultatAttendu)
    
    def test_extractNomTelephone(self):
        # GIVEN : préparer les données du test
        scraper = Scraper()
        extractor = Extractor()
        url = "https://phonesdata.com/fr/smartphones/apple/iphone-11-pro-5458276/"
        html = scraper.scrapUrl(url)
        resultatAttendu = "Apple iPhone 11 Pro"
        # WHEN : exécuter la fonction testée
        resultatObtenu = extractor.extractNomTelephone(html)
        # THEN : vérifier les résultats
        self.assertEqual(resultatObtenu, resultatAttendu)
    
    def test_traitementHtmlPrimaire(self):
        # GIVEN : préparer les données du test
        scraper = Scraper()
        extractor = Extractor()
        analyzer = Analyze()
        executor = Executor(scraper, extractor, analyzer)
        url = "https://phonesdata.com/fr/smartphones/"
        html = scraper.scrapUrl(url).find_all("p", {"class": "list-items"})
        resultatAttendu = ["https://phonesdata.com/fr/smartphones/apple/", "https://phonesdata.com/fr/smartphones/oneplus/"]
        # WHEN : exécuter la fonction testée
        resultatObtenu = [i for i in map(executor.traitementHtmlPrimaire, html) if i]
        # THEN : vérifier les résultats
        self.assertEqual(resultatObtenu, resultatAttendu)
    
    def test_traitementMarquesUrls(self):
        # GIVEN : préparer les données du test
        scraper = Scraper()
        extractor = Extractor()
        analyzer = Analyze()
        executor = Executor(scraper, extractor, analyzer)
        listBase = ["https://phonesdata.com/fr/smartphones/apple/", "https://phonesdata.com/fr/smartphones/oneplus/"]
        resultatAttendu = ['https://phonesdata.com/fr/smartphones/apple/#2019', 'https://phonesdata.com/fr/smartphones/apple/2018/', 'https://phonesdata.com/fr/smartphones/apple/2017/', 'https://phonesdata.com/fr/smartphones/apple/2016/', 'https://phonesdata.com/fr/smartphones/apple/2015/', 'https://phonesdata.com/fr/smartphones/apple/2014/', 'https://phonesdata.com/fr/smartphones/apple/2013/', 'https://phonesdata.com/fr/smartphones/apple/2012/', 'https://phonesdata.com/fr/smartphones/apple/2011/', 'https://phonesdata.com/fr/smartphones/apple/2010/', 'https://phonesdata.com/fr/smartphones/apple/2009/', 'https://phonesdata.com/fr/smartphones/apple/2008/', 'https://phonesdata.com/fr/smartphones/apple/2007/', 'https://phonesdata.com/fr/smartphones/oneplus/#2019', 'https://phonesdata.com/fr/smartphones/oneplus/2018/', 'https://phonesdata.com/fr/smartphones/oneplus/2017/', 'https://phonesdata.com/fr/smartphones/oneplus/2016/', 'https://phonesdata.com/fr/smartphones/oneplus/2015/', 'https://phonesdata.com/fr/smartphones/oneplus/2014/']
        # WHEN : exécuter la fonction testée
        resultatObtenu = [y for x in map(executor.traitementMarquesUrls, listBase) for y in x]
        # THEN : vérifier les résultats
        self.assertEqual(resultatObtenu, resultatAttendu)
    
    def test_traitementAnneesUrls(self):
        # GIVEN : préparer les données du test
        scraper = Scraper()
        extractor = Extractor()
        analyzer = Analyze()
        executor = Executor(scraper, extractor, analyzer)
        listBase = ['https://phonesdata.com/fr/smartphones/apple/#2019', 'https://phonesdata.com/fr/smartphones/apple/2018/', 'https://phonesdata.com/fr/smartphones/apple/2017/', 'https://phonesdata.com/fr/smartphones/apple/2016/', 'https://phonesdata.com/fr/smartphones/apple/2015/', 'https://phonesdata.com/fr/smartphones/apple/2014/', 'https://phonesdata.com/fr/smartphones/apple/2013/', 'https://phonesdata.com/fr/smartphones/apple/2012/', 'https://phonesdata.com/fr/smartphones/apple/2011/', 'https://phonesdata.com/fr/smartphones/apple/2010/', 'https://phonesdata.com/fr/smartphones/apple/2009/', 'https://phonesdata.com/fr/smartphones/apple/2008/', 'https://phonesdata.com/fr/smartphones/apple/2007/', 'https://phonesdata.com/fr/smartphones/oneplus/#2019', 'https://phonesdata.com/fr/smartphones/oneplus/2018/', 'https://phonesdata.com/fr/smartphones/oneplus/2017/', 'https://phonesdata.com/fr/smartphones/oneplus/2016/', 'https://phonesdata.com/fr/smartphones/oneplus/2015/', 'https://phonesdata.com/fr/smartphones/oneplus/2014/']
        resultatAttendu = ['https://phonesdata.com/fr/smartphones/apple/iphone-11-5458277/', 'https://phonesdata.com/fr/smartphones/apple/iphone-11-pro-5458276/', 'https://phonesdata.com/fr/smartphones/apple/iphone-11-pro-max-5458275/', 'https://phonesdata.com/fr/smartphones/apple/iphone-xr-5395/', 'https://phonesdata.com/fr/smartphones/apple/iphone-xs-5397/', 'https://phonesdata.com/fr/smartphones/apple/iphone-xs-max-5396/', 'https://phonesdata.com/fr/smartphones/apple/iphone-8-4895/', 'https://phonesdata.com/fr/smartphones/apple/iphone-8-plus-4894/', 'https://phonesdata.com/fr/smartphones/apple/iphone-x-4896/', 'https://phonesdata.com/fr/smartphones/apple/iphone-7-4361/', 'https://phonesdata.com/fr/smartphones/apple/iphone-7-plus-4362/', 'https://phonesdata.com/fr/smartphones/apple/iphone-se-4098/', 'https://phonesdata.com/fr/smartphones/apple/iphone-6s-3254/', 'https://phonesdata.com/fr/smartphones/apple/iphone-6s-plus-3255/', 'https://phonesdata.com/fr/smartphones/apple/iphone-6-2058/', 'https://phonesdata.com/fr/smartphones/apple/iphone-6-plus-2706/', 'https://phonesdata.com/fr/smartphones/apple/iphone-5c-103/', 'https://phonesdata.com/fr/smartphones/apple/iphone-5s-104/', 'https://phonesdata.com/fr/smartphones/apple/iphone-5-102/', 'https://phonesdata.com/fr/smartphones/apple/iphone-4-cdma-99/', 'https://phonesdata.com/fr/smartphones/apple/iphone-4s-101/', 'https://phonesdata.com/fr/smartphones/apple/iphone-4-100/', 'https://phonesdata.com/fr/smartphones/apple/iphone-3gs-98/', 'https://phonesdata.com/fr/smartphones/apple/iphone-3g-97/', 'https://phonesdata.com/fr/smartphones/apple/iphone-96/', 'https://phonesdata.com/fr/smartphones/oneplus/7-5808/', 'https://phonesdata.com/fr/smartphones/oneplus/7-pro-5807/', 'https://phonesdata.com/fr/smartphones/oneplus/7-pro-5g-5806/', 'https://phonesdata.com/fr/smartphones/oneplus/7t-5458362/', 'https://phonesdata.com/fr/smartphones/oneplus/7t-pro-5458372/', 'https://phonesdata.com/fr/smartphones/oneplus/7t-pro-5g-mclaren-5458402/', 'https://phonesdata.com/fr/smartphones/oneplus/6-5241/', 'https://phonesdata.com/fr/smartphones/oneplus/6t-5471/', 'https://phonesdata.com/fr/smartphones/oneplus/6t-mclaren-5511/', 'https://phonesdata.com/fr/smartphones/oneplus/5-4829/', 'https://phonesdata.com/fr/smartphones/oneplus/5t-5004/', 'https://phonesdata.com/fr/smartphones/oneplus/3-4245/', 'https://phonesdata.com/fr/smartphones/oneplus/3t-4522/', 'https://phonesdata.com/fr/smartphones/oneplus/2-3002/', 'https://phonesdata.com/fr/smartphones/oneplus/x-3738/', 'https://phonesdata.com/fr/smartphones/oneplus/one-2160/']
        # WHEN : exécuter la fonction testée
        resultatObtenu = [y for x in map(executor.traitementAnneesUrls, listBase) for y in x]
        # THEN : vérifier les résultats
        self.assertEqual(resultatObtenu, resultatAttendu)
    
    def test_extractBenchmarkLegende(self):
        # GIVEN : préparer les données du test
        scraper = Scraper()
        extractor = Extractor()
        url = "https://www.phonearena.com/phones/benchmarks"
        html = scraper.scrapUrl(url).find_all("div", {"class": "widget-benchmark"})[5]
        resultatAttendu = {'background-color: #FFCC51': 'AnTuTu - Higher is better', 'background-color: #A9DDE8': 'GFXBench T-Rex HD on-screen - Higher is better', 'background-color: #A1E84A': 'GFXBench Manhattan 3.1 on-screen - Higher is better', 'background-color: #4A61E8': 'Vellamo Metal - Higher is better', 'background-color: #FF7170': 'Basemark OS II - Higher is better', 'background-color: #FFA151': 'JetStream - Higher is better', 'background-color: #DBE84A': 'Geekbench 4 single-core - Higher is better', 'background-color: #FC35FF': 'Geekbench 4 multi-core - Higher is better'}
        # WHEN : exécuter la fonction testée
        resultatObtenu = extractor.extractBenchmarkLegende(html)
        # THEN : vérifier les résultats
        self.assertEqual(resultatObtenu, resultatAttendu)

    def test_lancerTraitement(self):
        # GIVEN : préparer les données du test
        scraper = Scraper()
        extractor = Extractor()
        analyzer = Analyze()
        executor = Executor(scraper, extractor, analyzer)
        url = "http://phonesdata.com/fr/smartphones/"
        resultatAttendu = pd.read_csv("/Users/omair/Desktop/M1/ProgAv2/Projet/test/temoin/marqueVise_Apple.csv", sep="\t").sort_index(inplace=True)
        # WHEN : exécuter la fonction testée
        resultatObtenu = executor.lancerTraitement(url).sort_index(inplace=True)
        # THEN : vérifier les résultats
        self.assertEqual(resultatObtenu, resultatAttendu)
    
    

unittest.main()