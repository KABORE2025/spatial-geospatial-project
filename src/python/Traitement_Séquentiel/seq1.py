import time
from pymongo import MongoClient
from pymongo import GEOSPHERE
import math

client = MongoClient('mongodb://localhost:27017')
db = client.BigData
collection = db.AUTOMOBILE

# Paramètres
product_name = "voiture_mercedes"
query_point = {"type": "Point", "coordinates": [-1.44, 12.35]}  # Ouagadougou
ref_lon, ref_lat = query_point["coordinates"]
R = 6371000

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

start_time = time.time()
results = collection.find({
    "produit": product_name,
    "localisation_site": {
        "$near": {
            "$geometry": query_point,
            "$maxDistance": 90000  # 90 km
        }
    }
})

print(f"Résultats pour '{product_name}' (rayon 5km):")
found = False
count = 0
for result in results:
    found = True
    count += 1
    doc_lon, doc_lat = result['localisation_site']['coordinates']
    distance = haversine(ref_lon, ref_lat, doc_lon, doc_lat)
#if count <= 10:
    print(f"Nom: {result['nom_entreprise']}, Produit: {result['produit']}, Quantité: {result['quantite_produit']}")
    print(f"Distance: {distance:.2f} mètres")
    print("-----")

if not found:
    print("Aucun document trouvé.")
end_time = time.time()
print(f"Nombre de résultats : {count}")
print(f"Temps d'exécution séquentiel : {(end_time - start_time):.4f} secondes")
client.close()