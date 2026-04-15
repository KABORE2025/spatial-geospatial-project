library(jsonlite)
library(sf)
library(dplyr)
library(ggplot2)

# 1. Lire le fichier JSON (structure liste de documents)
input_json <- "C:/Users/ZINA KARIM/python_projet/autre/ouaga.json"
raw_data <- fromJSON(input_json, simplifyVector = FALSE)

# 2. Extraire les coordonnées et construire une data frame
coords_list <- lapply(raw_data, function(doc) {
  c(lon = doc$localisation_site$coordinates[[1]],
    lat = doc$localisation_site$coordinates[[2]])
})
coords_df <- as.data.frame(do.call(rbind, coords_list))

# 3. Convertir en objet spatial
points_sf <- st_as_sf(coords_df, coords = c("lon", "lat"), crs = 4326)

# 4. Projection en UTM (Zone 30N)
points_sf_proj <- st_transform(points_sf, crs = 32630)

# 5. Création de la grille carrée
grid <- st_make_grid(points_sf_proj, cellsize = 7000, square = TRUE)
grid_sf <- st_sf(id = seq_along(grid), geometry = grid)

# 6. Associer chaque point à une cellule de la grille
points_with_cluster <- st_join(points_sf_proj, grid_sf, join = st_within)
points_with_cluster$cluster <- points_with_cluster$id

# 7. Ajouter les clusters dans les objets JSON d’origine
for (i in seq_along(raw_data)) {
  raw_data[[i]]$cluster <- points_with_cluster$cluster[i]
}

# 8. Sauvegarde JSON enrichi
write_json(raw_data, "C:/Users/ZINA KARIM/python_projet/autre/ouaga_cluster.json", 
           pretty = TRUE, auto_unbox = TRUE)

# 9. Export des shapefiles
st_write(points_with_cluster, "C:/Users/ZINA KARIM/python_projet/autre/ouaga_points_clusterises.shp", delete_layer = TRUE)
st_write(grid_sf, "C:/Users/ZINA KARIM/python_projet/autre/ouaga_grille_clusters.shp", delete_layer = TRUE)

# 10. Affichage graphique
ggplot() +
  geom_sf(data = grid_sf, fill = NA, color = "grey") +
  geom_sf(data = points_with_cluster, aes(color = as.factor(cluster))) +
  theme_minimal() +
  labs(title = "Visualisation des clusters sur la grille", color = "Cluster")

