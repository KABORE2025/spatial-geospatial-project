import os
import time
import math
from pymongo import MongoClient

# Paramètres
product_name = "voiture_mercedes"
query_point = [-1.44, 12.35]  # Point de référence [longitude, latitude]
R = 6371000  # Rayon de la Terre en mètres
nb_executions = 5  # Nombre d'exécutions pour la moyenne

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["BigData"]
collection = db["AUTOMOBILE"]

# Ajouter un index sur le champ "produit" (exécuter une seule fois)
collection.create_index("produit")

# Fonction Haversine
def haversine(lon1, lat1, lon2, lat2):
    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# Liste pour stocker les temps d'exécution
execution_times = []
filter_times = []
process_times = []

# Exécutions multiples
for i in range(nb_executions):
    start_time = time.time()

    # Étape 1 : Filtrage et comptage
    start_filter_time = time.time()
    total_count = collection.count_documents({"produit": product_name})
    filter_time = time.time() - start_filter_time

    # Étape 2 : Traitement (limite, distances, tri)
   
    start_process_time = time.time()
    results = collection.find({"produit": product_name})  # Sans limit
    distances = []
    for row in results:
        coords = row.get("localisation_site", {}).get("coordinates", [])
        if coords and len(coords) == 2:
            lon, lat = float(coords[0]), float(coords[1])
            distance = haversine(query_point[0], query_point[1], lon, lat) / 1000
            distances.append((row, distance))
        else:
            distances.append((row, None))


    # Trier par distance croissante
    distances.sort(key=lambda x: (x[1] is None, x[1]))
    process_time = time.time() - start_process_time
   

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)
    filter_times.append(filter_time)
    process_times.append(process_time)

    # Afficher les résultats
    print(f"\nExécution {i+1} :")
    print(f"{'Pos':<5} {'Nom':<20} {'Produit':<20} {'Ville':<15} {'Coordonnées':<35} {'Distance':<10}")
    print("-" * 105)
    for j, (row, distance) in enumerate(distances, 1):
        distance_str = f"{distance:.2f} km" if distance is not None else "Invalide"
        coords = row.get("localisation_site", {}).get("coordinates", [])
        print(f"{j:<5} {row.get('nom_entreprise', ''):<20} {row.get('produit', ''):<20} {row.get('ville', ''):<15} {str(coords):<35} {distance_str:<10}")
    print(f"Nombre total de lignes : {total_count}")
    print(f"Temps de filtrage : {filter_time:.4f} secondes")
    print(f"Temps de traitement : {process_time:.4f} secondes")
    print(f"Temps total d'exécution : {execution_time:.4f} secondes")

# Calculer les moyennes
avg_time = sum(execution_times) / nb_executions
avg_filter_time = sum(filter_times) / nb_executions
avg_process_time = sum(process_times) / nb_executions

# Afficher le résumé
print(f"\nRésumé :")
print(f"Nombre total de lignes trouvées : {total_count}")
print(f"Temps moyen de filtrage : {avg_filter_time:.4f} secondes")
print(f"Temps moyen de traitement : {avg_process_time:.4f} secondes")
print(f"Temps moyen total (sur {nb_executions} exécutions) : {avg_time:.4f} secondes")

# Fermer la connexion
client.close()