library(jsonlite)
library(sf)
library(dplyr)

# 1. Charger le JSON enrichi avec clusters
json_path <- "C:/Users/ZINA KARIM/python_projet/autre/ouaga_cluster.json"
raw_data <- fromJSON(json_path, simplifyVector = FALSE)

# 2. Extraire coordonnées
coords_list <- lapply(raw_data, function(doc) {
  c(lon = doc$localisation_site$coordinates[[1]],
    lat = doc$localisation_site$coordinates[[2]])
})
coords_df <- as.data.frame(do.call(rbind, coords_list))
points_sf <- st_as_sf(coords_df, coords = c("lon", "lat"), crs = 4326)
points_sf <- st_transform(points_sf, 32630)

# 3. Ajouter les clusters depuis JSON
clusters <- sapply(raw_data, function(doc) doc$cluster)
points_sf$cluster <- clusters

# 4. Séparer points valides et ceux à corriger
points_valide <- points_sf %>% filter(!is.na(cluster))
points_na <- points_sf %>% filter(is.na(cluster))

# 5. Trouver les plus proches voisins (pour points sans cluster)
nearest_idx <- st_nearest_feature(points_na, points_valide)

# 6. Récupérer les clusters des plus proches
clusters_corriges <- points_valide$cluster[nearest_idx]

# 7. Mise à jour dans la liste JSON
j <- 1
for (i in seq_along(raw_data)) {
  if (is.null(raw_data[[i]]$cluster)) {
    raw_data[[i]]$cluster <- clusters_corriges[j]
    j <- j + 1
  }
}

# 8. Sauvegarde du JSON corrigé
write_json(raw_data, "C:/Users/ZINA KARIM/python_projet/autre/ouaga_cluster_corrige.json",
           pretty = TRUE, auto_unbox = TRUE)

message("✅ Tous les documents ont maintenant un cluster assigné.")
