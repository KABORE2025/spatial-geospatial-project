import time
import math
from pymongo import MongoClient
from collections import defaultdict

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["BigData"]
collection = db["auto"]

# Paramètres
query_point = [-1.44, 12.35]
R = 6371000  # Rayon de la Terre en mètres
nb_executions = 5

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

# Exécutions multiples
execution_times = []
for i in range(nb_executions):
    start_time = time.time()

    # Compter les lignes totales
    total_count = collection.count_documents({})

    # Calculer les distances et statistiques
    city_stats = defaultdict(lambda: {"sum_distance": 0, "count": 0})
    for row in collection.find():
        coords = row.get("localisation_site", {}).get("coordinates", [])
        if coords and len(coords) == 2:
            try:
                lon, lat = float(coords[0]), float(coords[1])
                if abs(lon) > 180 or abs(lat) > 90:
                    continue
                distance = haversine(query_point[0], query_point[1], lon, lat) / 1000  # en km
                city = row.get("ville", "Unknown")
                city_stats[city]["sum_distance"] += distance
                city_stats[city]["count"] += 1
            except (ValueError, TypeError):
                continue

    # Calculer la distance moyenne par ville
    city_results = [
        {"ville": city, "avg_distance": stats["sum_distance"] / stats["count"], "count": stats["count"]}
        for city, stats in city_stats.items()
    ]
    # Trier par distance moyenne croissante
    city_results.sort(key=lambda x: x["avg_distance"])

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    # Afficher les résultats
    print(f"\nExécution {i+1} :")
    print(f"{'Pos':<5} {'Ville':<15} {'Distance Moyenne':<20} {'Nombre':<10}")
    print("-" * 55)
    for j, row in enumerate(city_results[:1000], 1):  # Limiter à 1000 pour l'affichage
        print(f"{j:<5} {row['ville']:<15} {row['avg_distance']:.2f} km{'':<10} {row['count']:<10}")
    print(f"Nombre total de lignes : {total_count}")
    print(f"Temps d'exécution : {execution_time:.4f} secondes")

# Calculer la moyenne
avg_time = sum(execution_times) / nb_executions
print(f"\nRésumé :")
print(f"Nombre total de lignes trouvées : {total_count}")
print(f"Temps moyen d'exécution (sur {nb_executions} exécutions) : {avg_time:.4f} secondes")

client.close()