library(jsonlite)
library(sf)
library(dplyr)

# Chargement du JSON d'origine
json_path <- "C:/Users/ZINA KARIM/python_projet/autre/ouaga_cluster.json"
data_json <- fromJSON(json_path, simplifyVector = FALSE)

# Chargement du shapefile de points (avec clusters)
points_sf <- st_read("C:/Users/ZINA KARIM/python_projet/autre/ouaga_points_clusterises.shp", quiet = TRUE)

# Chargement du shapefile de la grille
grille_sf <- st_read("C:/Users/ZINA KARIM/python_projet/autre/ouaga_grille_clusters.shp", quiet = TRUE)

# Calcul des voisins via st_touches (8-voisinage)
voisinage <- st_touches(grille_sf)

# Construction de la liste des voisins pour chaque cellule
grille_voisins <- lapply(seq_along(voisinage), function(i) {
  voisins <- grille_sf$id[voisinage[[i]]]
  list(cellule = grille_sf$id[i], voisins = setdiff(voisins, grille_sf$id[i]))
})

# Ajout du champ "voisins" dans les points
points_sf$voisins <- lapply(points_sf$id, function(cid) {
  v <- grille_voisins[[which(sapply(grille_voisins, function(x) x$cellule == cid))]]$voisins
  if (is.null(v)) NA else v
})

# Vérification
stopifnot(nrow(points_sf) == length(data_json))

# Fonction pour associer un document JSON à un point via les coordonnées GPS
find_point_index <- function(lon, lat, coords_matrix) {
  tol <- 1e-6
  match <- which(abs(coords_matrix[,1] - lon) < tol & abs(coords_matrix[,2] - lat) < tol)
  if (length(match) == 1) return(match)
  return(NA)
}

# Extraction des coordonnées GPS des points du shapefile
coords_sf <- st_coordinates(points_sf)

# Ajout du champ "voisins" à chaque document JSON
for (i in seq_along(data_json)) {
  coords <- data_json[[i]]$localisation_site$coordinates
  lon <- coords[[1]]
  lat <- coords[[2]]
  
  idx <- find_point_index(lon, lat, coords_sf)
  
  if (!is.na(idx)) {
    data_json[[i]]$voisins <- points_sf$voisins[[idx]]
  } else {
    data_json[[i]]$voisins <- NULL
  }
}

# Sauvegarde du nouveau fichier JSON enrichi
output_path <- "C:/Users/ZINA KARIM/python_projet/autre/ouaga_cluster_voisins.json"
write_json(data_json, output_path, pretty = TRUE, auto_unbox = TRUE)
message("✅ JSON enrichi avec les voisins correctement sauvegardé.")
