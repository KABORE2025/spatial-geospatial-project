import time
import math
from pymongo import MongoClient

# Paramètres
query_point = [-1.44, 12.35]  # Point de référence [longitude, latitude]
R = 6371000  # Rayon de la Terre en mètres
nb_executions = 5

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["BigData"]
collection = db["cluster"]

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
    return R * c / 1000  # en km

# Temps d'exécution
execution_times = []
for i in range(nb_executions):
    start_time = time.time()

    # Compter toutes les lignes
    total_count = collection.count_documents({})

    # Récupérer tous les documents et calculer les distances
    results = collection.find({})
    distances = []
    for row in results:
        coords = row.get("localisation_site", {}).get("coordinates", [])
        if coords and len(coords) == 2:
            lon, lat = float(coords[0]), float(coords[1])
            distance = haversine(query_point[0], query_point[1], lon, lat)
            distances.append((row, distance))
        else:
            distances.append((row, None))

    # Trier et prendre les 5 premiers
    distances.sort(key=lambda x: (x[1] is None, x[1]))
    top_5 = distances[:5]

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    # Afficher
    print(f"\nExécution {i+1} :")
    print(f"{'Pos':<5} {'Nom':<20} {'Produit':<20} {'Ville':<15} {'Coordonnées':<35} {'Distance':<10}")
    print("-" * 105)
    for j, (row, distance) in enumerate(top_5, 1):
        distance_str = f"{distance:.2f} km" if distance is not None else "Invalide"
        coords = row.get("localisation_site", {}).get("coordinates", [])
        print(f"{j:<5} {row.get('nom_entreprise', ''):<20} {row.get('produit', ''):<20} {row.get('ville', ''):<15} {str(coords):<35} {distance_str:<10}")
    print(f"Nombre total de lignes : {total_count}")
    print(f"Temps d'exécution : {execution_time:.4f} secondes")

# Moyenne
avg_time = sum(execution_times) / nb_executions
print(f"\nTemps moyen (sur {nb_executions} exécutions) : {avg_time:.4f} secondes")

client.close()