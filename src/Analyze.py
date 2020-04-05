import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from itertools import repeat
from config import config as cnf

class Analyze:

    def __init__(self):
        super().__init__()

    def genereGraph(self, graph, finalDF):
        cnf.logger.info("Génération du graphique {0}...".format(str(graph.__name__)))
        return graph(finalDF)
    
    def moyennePrixParAnGraph(self, finalDF):
        analyseDF = finalDF[["Date de sortie", "Prix approximatif"]].dropna()
        analyseDF["Date de sortie"] = analyseDF["Date de sortie"].str.split(",", expand=True)
        analyseDF[["Date de sortie"]] = analyseDF[["Date de sortie"]].astype(int)
        analyseDF["Prix approximatif"] = analyseDF["Prix approximatif"].str.replace(" EUR", "")
        analyseDF[["Prix approximatif"]] = analyseDF[["Prix approximatif"]].astype(float)
        analyseDF = analyseDF.set_index("Date de sortie")
        analyseDF["Date de sortie"] = analyseDF.index

        moyennePrixParAn = analyseDF.groupby(analyseDF["Date de sortie"])["Prix approximatif"].transform('mean')
        moyennePrixParAn = moyennePrixParAn.drop_duplicates().sort_index()
        
        fig = px.line(moyennePrixParAn, x=moyennePrixParAn.index, y="Prix approximatif", title="Évolution du prix des smartphones au fil des années")
        fig.update_layout(xaxis_title="Années", yaxis_title="Prix (en euros)")
        cnf.logger.info("Génération réussie")
        return fig
    
    def moyenneDureeBatterieParAnGraph(self, finalDF):
        analyseDF = finalDF[["Date de sortie", "Durée batterie"]].dropna()
        analyseDF["Date de sortie"] = analyseDF["Date de sortie"].str.split(",", expand=True)
        analyseDF[["Date de sortie"]] = analyseDF[["Date de sortie"]].astype(int)
        analyseDF[["Durée batterie"]] = analyseDF[["Durée batterie"]].astype(int)
        analyseDF = analyseDF.set_index("Date de sortie")
        analyseDF["Date de sortie"] = analyseDF.index
        
        moyenneDureeBatterieParAn = analyseDF.groupby(analyseDF["Date de sortie"])["Durée batterie"].transform('mean')
        moyenneDureeBatterieParAn = moyenneDureeBatterieParAn.drop_duplicates().sort_index()
        
        fig = px.line(moyenneDureeBatterieParAn, x=moyenneDureeBatterieParAn.index, y="Durée batterie", title="Évolution de l'autonomie des smartphones au fil des années")
        fig.update_layout(xaxis_title="Années", yaxis_title="Autonomie (en minutes)")
        cnf.logger.info("Génération réussie")
        return fig
    
    def moyenneTempsChargementParAnGraph(self, finalDF):
        analyseDF = finalDF[["Date de sortie", "Temps chargement"]].dropna()
        analyseDF["Date de sortie"] = analyseDF["Date de sortie"].str.split(",", expand=True)
        analyseDF[["Date de sortie"]] = analyseDF[["Date de sortie"]].astype(int)
        analyseDF[["Temps chargement"]] = analyseDF[["Temps chargement"]].astype(int)
        analyseDF = analyseDF.set_index("Date de sortie")
        analyseDF["Date de sortie"] = analyseDF.index
        
        moyenneTempsChargementParAn = analyseDF.groupby(analyseDF["Date de sortie"])["Temps chargement"].transform('mean')
        moyenneTempsChargementParAn = moyenneTempsChargementParAn.drop_duplicates().sort_index()
        
        fig = px.line(moyenneTempsChargementParAn, x=moyenneTempsChargementParAn.index, y="Temps chargement", title="Évolution de la durée de chargement des smartphones au fil des années")
        fig.update_layout(xaxis_title="Années", yaxis_title="Durée chargement (en minutes)")
        cnf.logger.info("Génération réussie")
        return fig

    def repartitionPrixSmartphoneGraph(self, finalDF):
        analyseDF = finalDF[["Prix approximatif"]].dropna()
        analyseDF["Prix approximatif"] = analyseDF["Prix approximatif"].str.replace(" EUR", "")
        analyseDF[["Prix approximatif"]] = analyseDF[["Prix approximatif"]].astype(float)

        borneInf = [1, 101, 201, 301, 401, 501, 601, 701, 801, 901, 1001, 1101, 1201]
        borneSup = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 9999]

        repartitionPrixSmartphoneJson = {}
        for i in range(len(borneInf)):
            repartitionPrixSmartphoneJson.update(self.getPourcentagePrice(analyseDF, repartitionPrixSmartphoneJson, borneInf[i], borneSup[i]))

        repartitionPrixSmartphone = pd.DataFrame(repartitionPrixSmartphoneJson, index=["Pourcentage"]).transpose()

        fig = px.bar(repartitionPrixSmartphone, x=repartitionPrixSmartphone.index, y="Pourcentage", title="Répartition des prix des smartphones")
        fig.update_layout(xaxis_title="Tranche de prix", yaxis_title="Pourcentage (%)")
        cnf.logger.info("Génération réussie")
        return fig

    def getPourcentagePrice(self, df, repartitionPrixSmartphoneJson, borneInf, borneSup):
        key = "De {0}€ à {1}€".format(borneInf, borneSup)
        try:
            repartitionPrixSmartphoneJson[key] = (df["Prix approximatif"].between(borneInf, borneSup).value_counts(normalize=True) * 100)[True]
        except KeyError:
            repartitionPrixSmartphoneJson[key] = 0
        return repartitionPrixSmartphoneJson

    def repartitionOSGraph(self, finalDF):
        analyseDF = finalDF[["Système d'exploitation (OS)"]].dropna()
        analyseDF["Système d'exploitation (OS)"] = analyseDF["Système d'exploitation (OS)"].str.split(expand=True)
        analyseDF["Système d'exploitation (OS)"] = analyseDF["Système d'exploitation (OS)"].str.split(",", expand=True)
        analyseDF["Système d'exploitation (OS)"] = analyseDF["Système d'exploitation (OS)"].str.capitalize() 
        repartitionOSGraph = (analyseDF["Système d'exploitation (OS)"].value_counts(normalize=True) * 100)
        
        fig = px.pie(repartitionOSGraph, values="Système d'exploitation (OS)", names=repartitionOSGraph.index, title="Répartition des systèmes d'exploitation des smartphones")
        fig.update_traces(textposition='inside')
        cnf.logger.info("Génération réussie")
        return fig