import os
import time
import math
from pyspark.sql import SparkSession

# Configurer les variables d'environnement
os.environ["PYSPARK_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk1.8.0_192"
os.environ["SPARK_HOME"] = "C:\\Spark\\spark-3.5.3-bin-hadoop3"

# Initialiser SparkSession
spark = SparkSession.builder \
    .appName("MongoQueryWithDistance") \
    .master("local[*]") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/BigData.AUTOMOBILE") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Paramètres
product_name = "voiture_mercedes"
query_point = [-1.44, 12.35]  # Point de référence [longitude, latitude]
R = 6371000  # Rayon de la Terre en mètres
nb_executions = 5  # Nombre d'exécutions pour la moyenne

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

# Charger les données une fois et les mettre en cache
df = spark.read.format("mongo").load()
filtered_df = df.filter(df.produit == product_name).cache()

# Liste pour stocker les temps d'exécution
execution_times = []

# Exécutions multiples
for i in range(nb_executions):
    start_time = time.time()

    # Compter les lignes totales
    total_count = filtered_df.count()

    # Récupérer les 5 premières lignes et calculer les distances
    results = filtered_df.select("nom_entreprise", "produit", "ville", "localisation_site.coordinates").limit(5).collect()
    distances = []
    for row in results:
        coords = row["coordinates"]
        if coords and len(coords) == 2:
            lon, lat = float(coords[0]), float(coords[1])
            distance = haversine(query_point[0], query_point[1], lon, lat) / 1000  # en km
            distances.append((row, distance))
        else:
            distances.append((row, None))

    # Trier par distance croissante (None sera placé à la fin)
    distances.sort(key=lambda x: (x[1] is None, x[1]))

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    # Afficher les résultats sous forme de tableau simple
    print(f"\nExécution {i+1} :")
    print(f"{'Pos':<5} {'Nom':<20} {'Produit':<20} {'Ville':<15} {'Coordonnées':<35} {'Distance':<10}")
    print("-" * 105)
    for j, (row, distance) in enumerate(distances, 1):
        distance_str = f"{distance:.2f} km" if distance is not None else "Invalide"
        print(f"{j:<5} {row['nom_entreprise']:<20} {row['produit']:<20} {row['ville']:<15} {str(row['coordinates']):<35} {distance_str:<10}")
    print(f"Nombre total de lignes : {total_count}")
    print(f"Temps d'exécution : {execution_time:.4f} secondes")

# Calculer la moyenne
avg_time = sum(execution_times) / nb_executions

# Afficher le résumé final
print(f"\nRésumé :")
print(f"Nombre total de lignes trouvées : {total_count}")
print(f"Temps moyen d'exécution (sur {nb_executions} exécutions) : {avg_time:.4f} secondes")

# Arrêter Spark
spark.stop()