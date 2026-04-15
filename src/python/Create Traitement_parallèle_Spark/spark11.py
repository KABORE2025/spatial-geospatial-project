import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, avg, count

# Configurer les variables d'environnement
os.environ["PYSPARK_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk1.8.0_192"
os.environ["SPARK_HOME"] = "C:\\Spark\\spark-3.5.3-bin-hadoop3"

# Initialiser SparkSession
spark = SparkSession.builder \
    .appName("MongoQueryStatsParallel") \
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
query_point = [-1.44, 12.35]
R = 6371  # Rayon de la Terre en km
nb_executions = 5

# Charger les données
df = spark.read.format("mongo").load().repartition(200).cache()

# Pré-filtrer les documents avec des coordonnées valides
df = df.filter(
    (col("localisation_site.coordinates").isNotNull()) &
    (col("localisation_site.coordinates").getItem(0).isNotNull()) &
    (col("localisation_site.coordinates").getItem(1).isNotNull()) &
    (col("localisation_site.coordinates").getItem(0).cast("float").between(-180, 180)) &
    (col("localisation_site.coordinates").getItem(1).cast("float").between(-90, 90))
)

total_count = df.count()
print(f"Nombre total de documents : {total_count}")

# Exécutions multiples
execution_times = []
for i in range(nb_executions):
    start_time = time.time()

    # Calculer les distances
    df_with_distance = df.withColumn(
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

    # Calculer la distance moyenne et le nombre d'entreprises par ville
    stats_df = df_with_distance.groupBy("ville") \
                               .agg(
                                   avg("distance").alias("avg_distance"),
                                   count("*").alias("count")
                               ) \
                               .orderBy("avg_distance")

    # Récupérer un échantillon pour l'affichage
    results = stats_df.limit(1000).collect()

    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)

    # Afficher les résultats
    print(f"\nExécution {i+1} :")
    print(f"{'Pos':<5} {'Ville':<15} {'Distance Moyenne':<20} {'Nombre':<10}")
    print("-" * 55)
    for j, row in enumerate(results, 1):
        print(f"{j:<5} {row['ville']:<15} {row['avg_distance']:.2f} km{'':<10} {row['count']:<10}")
    print(f"Temps d'exécution : {execution_time:.4f} secondes")

# Calculer la moyenne
avg_time = sum(execution_times) / nb_executions
print(f"\nRésumé :")
print(f"Temps moyen d'exécution (sur {nb_executions} exécutions) : {avg_time:.4f} secondes")

spark.stop()