import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Analyze:

    def __init__(self):
        super().__init__()
    
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
        return fig

    def repartitionPrixSmartphoneGraph(self, finalDF):
        analyseDF = finalDF[["Prix approximatif"]].dropna()
        analyseDF["Prix approximatif"] = analyseDF["Prix approximatif"].str.replace(" EUR", "")
        analyseDF[["Prix approximatif"]] = analyseDF[["Prix approximatif"]].astype(float)

        repartitionPrixSmartphoneJson = {}
        repartitionPrixSmartphoneJson["De 1€ à 101€"] = (analyseDF["Prix approximatif"].between(1, 100).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 101€ à 200€"] = (analyseDF["Prix approximatif"].between(101, 200).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 201€ à 300€"] = (analyseDF["Prix approximatif"].between(201, 300).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 301€ à 400€"] = (analyseDF["Prix approximatif"].between(301, 400).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 401€ à 500€"] = (analyseDF["Prix approximatif"].between(401, 500).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 501€ à 600€"] = (analyseDF["Prix approximatif"].between(501, 600).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 601€ à 700€"] = (analyseDF["Prix approximatif"].between(601, 700).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 701€ à 800€"] = (analyseDF["Prix approximatif"].between(701, 800).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 801€ à 900€"] = (analyseDF["Prix approximatif"].between(801, 900).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 901€ à 1000€"] = (analyseDF["Prix approximatif"].between(901, 1000).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 1001€ à 1100€"] = (analyseDF["Prix approximatif"].between(1001, 1100).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["De 1101€ à 1200€"] = (analyseDF["Prix approximatif"].between(1101, 1200).value_counts(normalize=True) * 100)[True]
        repartitionPrixSmartphoneJson["Plus de 1200€"] = (analyseDF["Prix approximatif"].between(1201, 99999).value_counts(normalize=True) * 100)[True]
        
        repartitionPrixSmartphone = pd.DataFrame(repartitionPrixSmartphoneJson, index=["Pourcentage"]).transpose()

        print(repartitionPrixSmartphone)
        #fig = px.pie(repartitionPrixSmartphone, values="Pourcentage", names=repartitionPrixSmartphone.index, title="Répartition des prix des smartphones")
        fig = px.bar(repartitionPrixSmartphone, x=repartitionPrixSmartphone.index, y="Pourcentage", title="Répartition des prix des smartphones")
        fig.update_layout(xaxis_title="Tranche de prix", yaxis_title="Pourcentage (%)")
        return fig

    def repartitionOSGraph(self, finalDF):
        analyseDF = finalDF[["Système d'exploitation (OS)"]].dropna()
        analyseDF["Système d'exploitation (OS)"] = analyseDF["Système d'exploitation (OS)"].str.split(expand=True)
        analyseDF["Système d'exploitation (OS)"] = analyseDF["Système d'exploitation (OS)"].str.split(",", expand=True)
        analyseDF["Système d'exploitation (OS)"] = analyseDF["Système d'exploitation (OS)"].str.capitalize() 
        repartitionOSGraph = (analyseDF["Système d'exploitation (OS)"].value_counts(normalize=True) * 100)
        
        fig = px.pie(repartitionOSGraph, values="Système d'exploitation (OS)", names=repartitionOSGraph.index, title="Répartition des systèmes d'exploitation des smartphones")
        fig.update_traces(textposition='inside')
        return fig