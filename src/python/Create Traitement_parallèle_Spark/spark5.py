import os
import time
import math
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType

# Configurer les variables d'environnement
os.environ["PYSPARK_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk1.8.0_192"
os.environ["SPARK_HOME"] = "C:\\Spark\\spark-3.5.3-bin-hadoop3"

# Initialiser SparkSession
spark = SparkSession.builder \
    .appName("MongoQueryFullDistance") \
    .master("local[*]") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/BigData.AUTOMOBILE") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Paramètres
query_point = [-1.44, 12.35]  # Point de référence [longitude, latitude]
R = 6371000  # Rayon de la Terre en mètres
nb_executions = 5

# Fonction Haversine robuste comme UDF
def haversine(lon, lat):
    try:
        if lon is None or lat is None or not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)):
            return None
        lon1_rad = math.radians(query_point[0])
        lat1_rad = math.radians(query_point[1])
        lon2_rad = math.radians(float(lon))
        lat2_rad = math.radians(float(lat))
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c / 1000  # en km
    except Exception:
        return None

haversine_udf = udf(haversine, FloatType())

# Charger les données et ajouter la colonne distance
df = spark.read.format("mongo").load()
df_with_distance = df.withColumn("distance", haversine_udf(df["localisation_site.coordinates"][0], df["localisation_site.coordinates"][1])).cache()

# Temps d'exécution
execution_times = []
for i in range(nb_executions):
    start_time = time.time()

    # Compter toutes les lignes
    total_count = df_with_distance.count()

    # Trier par distance et prendre les 5 premiers
    results = df_with_distance.select("nom_entreprise", "produit", "ville", "localisation_site.coordinates", "distance") \
                              .orderBy("distance").limit(5).collect()

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    # Afficher
    print(f"\nExécution {i+1} :")
    print(f"{'Pos':<5} {'Nom':<20} {'Produit':<20} {'Ville':<15} {'Coordonnées':<35} {'Distance':<10}")
    print("-" * 105)
    for j, row in enumerate(results, 1):
        distance_str = f"{row['distance']:.2f} km" if row['distance'] is not None else "Invalide"
        print(f"{j:<5} {row['nom_entreprise']:<20} {row['produit']:<20} {row['ville']:<15} {str(row['coordinates']):<35} {distance_str:<10}")
    print(f"Nombre total de lignes : {total_count}")
    print(f"Temps d'exécution : {execution_time:.4f} secondes")

# Moyenne
avg_time = sum(execution_times) / nb_executions
print(f"\nTemps moyen (sur {nb_executions} exécutions) : {avg_time:.4f} secondes")

spark.stop()