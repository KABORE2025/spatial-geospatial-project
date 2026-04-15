# Ajout des bibliothèques nécessaires
library(ggplot2)    # Pour le traitement du graphe
library(cluster)    # Analyse K-Means
library(factoextra) # Visualisation de l'analyse
library(jsonlite)   # Pour lire et écrire des fichiers JSON
library(sf)         # Pour gérer les géométries spatiales et exporter en Shapefile
library(deldir)     # Pour générer les diagrammes de Voronoï

# Vérifier et installer les packages nécessaires
required_packages <- c("ggplot2", "cluster", "factoextra", "jsonlite", "sf", "deldir")
for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
    library(pkg, character.only = TRUE)
  }
}

# Définir la reproductibilité
set.seed(1)

# Étape 1 : Charger les données à partir du fichier JSON
json_file_path <- "C:/Users/ZINA KARIM/python_projet/autre/ouaga.json"  # Chemin de ton fichier JSON
print(paste("Lecture du fichier JSON :", json_file_path))

# Vérifier si le fichier existe
if (!file.exists(json_file_path)) {
  stop(paste("Le fichier", json_file_path, "n'existe pas."))
}

# Charger le fichier JSON
data <- fromJSON(json_file_path)

# Vérifier si les données sont une liste ou un objet unique
if (!is.list(data) || !is.data.frame(data)) {
  data <- as.data.frame(data)  # Convertir en data.frame si c’est un objet unique
}

# Normaliser les données imbriquées (ex. : localisation_site.coordinates)
df <- data.frame(
  nom_entreprise = data$nom_entreprise,
  type_marque = data$type_marque,
  quantite = as.numeric(data$quantite),
  ville = data$ville,
  arrondissement = data$arrondissement,
  secteur = as.numeric(gsub("[^0-9.]", "", data$secteur)),  # Convertir secteur en numérique
  longitude = sapply(data$localisation_site$coordinates, function(x) x[1]),
  latitude = sapply(data$localisation_site$coordinates, function(x) x[2])
)

# Afficher les premières lignes pour vérification
print("Données initiales :")
print(head(df))

# Filtrer les données pour le Burkina Faso (facultatif, selon tes besoins)
df <- df[df$latitude >= 9.5 & df$latitude <= 15.0 & df$longitude >= -5.5 & df$longitude <= 2.5, ]

# Préparer les données pour le clustering (uniquement latitude et longitude)
donnees_clustering <- df[, c("latitude", "longitude")]

# Étape 2 : Tracer la courbe Elbow pour déterminer le nombre optimal de clusters
t <- numeric(10)  # Initialiser le vecteur t pour stocker l'inertie
for (k in 1:10) {
  kmeans_result <- kmeans(donnees_clustering, centers = k, nstart = 25)
  t[k] <- sum(kmeans_result$tot.withinss)  # Somme des carrés intra-cluster
}

# Tracer la courbe Elbow
plot(1:10, t, type = "b", pch = 19, frame = FALSE,
     xlab = "Nombre de clusters (k)",
     ylab = "Somme des carrés intra-cluster (WSS)",
     main = "Courbe Elbow pour déterminer le nombre optimal de clusters")
abline(v = 4, col = "red", lty = 2)

# Étape 3 : Appliquer K-Means avec le nombre optimal de clusters
k_optimal <- 9 # Choix basé sur la courbe Elbow (à ajuster après visualisation)
kmeans_result <- kmeans(donnees_clustering, centers = k_optimal, nstart = 25)
cat("Centres des clusters :\n")
print(kmeans_result$centers)

# Étape 4 : Ajouter les clusters aux données
df$cluster <- as.factor(kmeans_result$cluster)  # Ajouter la colonne cluster
print("Données avec clusters :")
print(head(df))

# Étape 5 : Exportation des fichiers pour MongoDB et QGIS

# 5.1 : Sauvegarder les données avec clusters dans un fichier JSON pour MongoDB
json_output_path <- "C:/Users/ZINA KARIM/python_projet/kcluster/ouaga_with_clusters.json"
json_data <- list()
for (i in 1:nrow(df)) {
  doc <- list(
    nom_entreprise = df$nom_entreprise[i],
    type_marque = df$type_marque[i],
    quantite = as.integer(df$quantite[i]),
    ville = df$ville[i],
    arrondissement = df$arrondissement[i],
    secteur = as.numeric(df$secteur[i]),
    location = list(
      type = "Point",
      coordinates = c(df$longitude[i], df$latitude[i])
    ),
    cluster = as.integer(as.character(df$cluster[i]))
  )
  json_data[[i]] <- doc
}
write_json(json_data, json_output_path, pretty = TRUE, auto_unbox = TRUE)
cat("Fichier JSON avec clusters généré pour MongoDB :", json_output_path, "\n")

# 5.2 : Générer des fichiers Shapefile pour QGIS
# Créer le répertoire de sortie s’il n’existe pas
output_dir <- "C:/Users/ZINA KARIM/python_projet/kcluster"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Définir une fenêtre d'extension (bounding box) pour couvrir tous les points
# Ajouter une marge pour s'assurer que tous les points sont inclus
margin <- 0.1  # Marge de 0.1 degré autour des points
rw <- c(
  min(df$longitude) - margin,
  max(df$longitude) + margin,
  min(df$latitude) - margin,
  max(df$latitude) + margin
)
cat("Fenêtre d'extension pour les Voronoï (rw) :", rw, "\n")

# Shapefile des points (entreprises)
gdf_points <- st_as_sf(df, coords = c("longitude", "latitude"), crs = 4326)
points_shp_path <- file.path(output_dir, "entreprises_points.shp")
st_write(gdf_points, points_shp_path, delete_layer = TRUE)
cat("Shapefile des points généré :", points_shp_path, "\n")

# Shapefile des centres (centroids)
centroids_df <- as.data.frame(kmeans_result$centers)
centroids_df$cluster_id <- 1:k_optimal
gdf_centroids <- st_as_sf(centroids_df, coords = c("longitude", "latitude"), crs = 4326)
centroids_shp_path <- file.path(output_dir, "centroids.shp")
st_write(gdf_centroids, centroids_shp_path, delete_layer = TRUE)
cat("Shapefile des centroids généré :", centroids_shp_path, "\n")

# Générer les cellules de Voronoï avec une fenêtre d'extension
vor <- deldir(centroids_df$longitude, centroids_df$latitude, rw = rw)
vor_tiles <- tile.list(vor)
polygons <- lapply(vor_tiles, function(tile) {
  coords <- cbind(c(tile$x, tile$x[1]), c(tile$y, tile$y[1]))
  if (length(unique(coords)) < 4 || any(is.na(coords))) {
    return(NULL)
  }
  st_polygon(list(coords))
})
polygons <- Filter(Negate(is.null), polygons)
vor_sf <- st_sfc(polygons, crs = 4326)
vor_df <- st_sf(data.frame(cluster_id = 1:length(vor_sf)), geometry = vor_sf)
voronoi_shp_path <- file.path(output_dir, "voronoi_cells.shp")
st_write(vor_df, voronoi_shp_path, delete_layer = TRUE)
cat("Shapefile des cellules de Voronoï généré :", voronoi_shp_path, "\n")

