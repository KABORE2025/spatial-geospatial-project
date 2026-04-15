import os
import time
from pyspark.sql import SparkSession

# Configurer les variables d'environnement
#os.environ["PYSPARK_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
#os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe"
#os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk1.8.0_192"
#os.environ["SPARK_HOME"] = "C:\\Spark\\spark-3.5.3-bin-hadoop3"

# Initialiser SparkSession
spark = SparkSession.builder \
    .appName("SimpleMongoQueryWithSpark") \
    .master("local[*]") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/BigData.AUTOMOBILE") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.pyspark.python", "C:/Users/ZINA KARIM/AppData/Local/Programs/Python/Python313/python.exe") \
    .getOrCreate()

# Paramètre de recherche
product_name = "voiture_mercedes"

# Chronométrage
start_time = time.time()

# Charger les données depuis MongoDB
df = spark.read.format("mongo").load()

# Filtrer les données
filtered_df = df.filter(df.produit == product_name)

# Compter les lignes
count = filtered_df.count()

# Temps d'exécution
end_time = time.time()
execution_time = end_time - start_time

# Afficher les résultats
print(f"Nombre de lignes trouvées pour '{product_name}' : {count}")
print(f"Temps d'exécution avec Spark : {execution_time:.4f} secondes")

# Optionnel : Afficher un aperçu des résultats
filtered_df.show(5, truncate=False)

# Arrêter Spark
spark.stop()