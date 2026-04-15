from pymongo import MongoClient
import time

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["BigData"]
collection = db["Auto2"]

# Liste des requêtes à comparer
requêtes = {
    "Recherche par entreprise": {"nom_entreprise": "Vendeur de véhicules d’occasion"},
    "Recherche par cluster": {"cluster": 3},
    "Recherche par coordonnées": {
        "localisation_site": {
            "$near": {
                "$geometry": {     
                    "type": "Point",
                    "coordinates": [-1.4995, 12.3422]
                },
                "$maxDistance": 2000  # Rayon de 7 km par exemple
            }
        }
    },
    "Recherche dans un voisinage": {"cluster": {"$in": [2, 4, 6, 7, 8]}}
}

# Fonction d'analyse de requête avec `explain`
def analyser_requête(nom, filtre):
    print(f"\n🔍 {nom}")
    début = time.time()
    plan = collection.find(filtre).explain()
    fin = time.time()
    
    stats = plan['executionStats']
    print(f"Temps d'exécution (s) : {round(fin - début, 4)}")
    print(f"Nombre de documents examinés : {stats['totalDocsExamined']}")
    print(f"Nombre de documents retournés : {stats['nReturned']}")
    print(f"Plan utilisé : {stats.get('executionStages', {}).get('stage', 'N/A')}")

# Exécution des requêtes
for nom, filtre in requêtes.items():
    analyser_requête(nom, filtre)
