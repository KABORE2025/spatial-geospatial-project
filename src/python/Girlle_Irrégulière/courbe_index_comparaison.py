import pymongo
import random
from statistics import mean
from pprint import pprint

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["BigData"]
collection = db["Auto"]

# Fonction pour insérer des données supplémentaires (facultatif)
def insert_sample_data(num_docs):
    for i in range(num_docs):
        lon = -1.529 + random.uniform(-0.5, 0.5)  # ±0.5 degrés (~55 km)
        lat = 12.295 + random.uniform(-0.5, 0.5)
        doc = {
            "location": {"type": "Point", "coordinates": [lon, lat]},
            "cluster": str(random.randint(1, 10)),  # Clusters de 1 à 10
            "neighbors": [str(random.randint(1, 10)) for _ in range(random.randint(1, 5))]  # Liste de voisins
        }
        collection.insert_one(doc)
    print(f"{num_docs} documents insérés.")

# Fonction pour exécuter une requête et collecter les métriques
def run_query(query, num_runs=100):
    times = []
    n_returned = []
    docs_examined = []
    keys_examined = []
    
    for _ in range(num_runs):
        explain_result = collection.find(query).explain()
        stats = explain_result["executionStats"]
        times.append(stats["executionTimeMillis"])
        n_returned.append(stats["nReturned"])
        docs_examined.append(stats["totalDocsExamined"])
        keys_examined.append(stats["totalKeysExamined"])
    
    return {
        "avg_executionTimeMillis": mean(times),
        "avg_nReturned": mean(n_returned),
        "avg_totalDocsExamined": mean(docs_examined),
        "avg_totalKeysExamined": mean(keys_examined)
    }

# Définir les quatre requêtes
query1 = {
    "location": {
        "$near": {
            "$geometry": {"type": "Point", "coordinates": [-1.529, 12.295]},
            "$maxDistance": 50000
        }
    }
}

query2 = {
    "$or": [
        {"cluster": "7"},
        {"neighbors": {"$in": ["7", "8", "9"]}},
        {"cluster": "8"}
    ]
}

query3 = {
    "location": {
        "$near": {
            "$geometry": {"type": "Point", "coordinates": [-1.529, 12.295]},
            "$maxDistance": 50000
        }
    },
    "$or": [
        {"cluster": "7"},
        {"neighbors": {"$in": ["7", "8", "9"]}},
        {"cluster": "8"}
    ]
}

query4 = {
    "neighbors": {"$in": ["7", "8", "9"]}
}

# (Facultatif) Insérer des données pour augmenter la charge
# insert_sample_data(10000)  # Décommente pour insérer 10 000 documents

# Exécuter les quatre algorithmes
print("Exécution de l'Algorithme 1 (location_2dsphere)...")
results1 = run_query(query1)
print("Exécution de l'Algorithme 2 (neighbors_1 + cluster_1_neighbors_1)...")
results2 = run_query(query2)
print("Exécution de l'Algorithme 3 (location_2dsphere + neighbors_1)...")
results3 = run_query(query3)
print("Exécution de l'Algorithme 4 (neighbors_1)...")
results4 = run_query(query4)

# Afficher les résultats textuels
print("\nRésultats comparatifs :")
print("=====================")
print("Algorithme 1 (location_2dsphere) :")
pprint(results1)
print("\nAlgorithme 2 (neighbors_1 + cluster_1_neighbors_1) :")
pprint(results2)
print("\nAlgorithme 3 (location_2dsphere + neighbors_1) :")
pprint(results3)
print("\nAlgorithme 4 (neighbors_1) :")
pprint(results4)

# Comparaison rapide (Algorithme 3 vs Algorithme 1)
print("\nDifférences clés (Algo 3 vs Algo 1) :")
print(f"Différence de temps (Algo 3 - Algo 1) : {results3['avg_executionTimeMillis'] - results1['avg_executionTimeMillis']:.2f} ms")
print(f"Différence de documents examinés (Algo 3 - Algo 1) : {results3['avg_totalDocsExamined'] - results1['avg_totalDocsExamined']:.0f}")