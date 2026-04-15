import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, when

# Configurer les variables d'environnement
os.environ["PYSPARK_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk1.8.0_192"
os.environ["SPARK_HOME"] = "C:\\Spark\\spark-3.5.3-bin-hadoop3"

# Initialiser SparkSession avec optimisations
spark = SparkSession.builder \
    .appName("MongoQueryWithDistanceParallel") \
    .master("local[*]") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/BigData.auto") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.sql.shuffle.partitions", 200) \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .getOrCreate()

# Paramètres
product_name = "voiture_mercedes"
query_point = [-1.44, 12.35]
R = 6371  # Rayon de la Terre en km (changé pour cohérence avec km)
nb_executions = 5

# Charger les données et les mettre en cache
df = spark.read.format("mongo").load()
filtered_df = df.filter(col("produit") == product_name) \
                .repartition(200) \
                .cache()

# Pré-filtrer les documents avec des coordonnées valides
filtered_df = filtered_df.filter(
    (col("localisation_site.coordinates").isNotNull()) &
    (col("localisation_site.coordinates").getItem(0).isNotNull()) &
    (col("localisation_site.coordinates").getItem(1).isNotNull()) &
    (col("localisation_site.coordinates").getItem(0).cast("float").between(-180, 180)) &
    (col("localisation_site.coordinates").getItem(1).cast("float").between(-90, 90))
)

total_count = filtered_df.count()  # Compter une seule fois
print(f"Nombre total de documents filtrés : {total_count}")

# Exécutions multiples
execution_times = []
for i in range(nb_executions):
    start_time = time.time()

    # Calculer les distances en utilisant Spark SQL (sans UDF Python)
    df_with_distance = filtered_df.withColumn(
        "distance",
        expr(f"""
            {R} * 2 * ASIN(SQRT(
                SIN(RADIANS({query_point[1]} - localisation_site.coordinates[1])/2) * 
                SIN(RADIANS({query_point[1]} - localisation_site.coordinates[1])/2) + 
                COS(RADIANS({query_point[1]})) * COS(RADIANS(localisation_site.coordinates[1])) * 
                SIN(RADIANS({query_point[0]} - localisation_site.coordinates[0])/2) * 
                SIN(RADIANS({query_point[0]} - localisation_site.coordinates[0])/2)
            ))
        """)
    )

    # Trier et limiter les résultats
    df_with_distance = df_with_distance.filter(col("distance").isNotNull()) \
                                       .select("nom_entreprise", "produit", "ville", "localisation_site.coordinates", "distance") \
                                       .orderBy("distance")

    # Récupérer un échantillon pour l'affichage
    results = df_with_distance.limit(1000).collect()

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    # Afficher les résultats
    print(f"\nExécution {i+1} :")
    print(f"{'Pos':<5} {'Nom':<20} {'Produit':<20} {'Ville':<15} {'Coordonnées':<35} {'Distance':<10}")
    print("-" * 105)
    for j, row in enumerate(results, 1):
        distance_str = f"{row['distance']:.2f} km" if row['distance'] is not None else "Invalide"
        print(f"{j:<5} {row['nom_entreprise']:<20} {row['produit']:<20} {row['ville']:<15} {str(row['coordinates']):<35} {distance_str:<10}")
    print(f"Temps d'exécution : {execution_time:.4f} secondes")

# Calculer la moyenne
avg_time = sum(execution_times) / nb_executions
print(f"\nRésumé :")
print(f"Nombre total de lignes trouvées : {total_count}")
print(f"Temps moyen d'exécution (sur {nb_executions} exécutions) : {avg_time:.4f} secondes")

spark.stop()