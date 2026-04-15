# Charger les packages nécessaires
library(sf)
library(jsonlite)
library(mongolite)

# Connexion à MongoDB
mongo <- mongo(collection = "Auto", db = "BigData", url = "mongodb://localhost:27017/")

# Chemins des fichiers
voronoi_shp <- "C:/Users/ZINA KARIM/python_projet/kcluster/voronoi_cells.shp"  # Fichier SHP des cellules de Voronoï
centers_shp <- "C:/Users/ZINA KARIM/python_projet/kcluster/centroids.shp"      # Fichier SHP des centres des clusters
json_file <- "C:/Users/ZINA KARIM/python_projet/kcluster/ouaga_with_clusters.json"  # Fichier JSON contenant les données

# Lire les fichiers SHP
voronoi_cells <- st_read(voronoi_shp)
cluster_centers <- st_read(centers_shp)

# Vérifier la validité des géométries
voronoi_cells <- st_make_valid(voronoi_cells)  # Réparer les géométries invalides
print(summary(voronoi_cells))  # Vérifier la structure des données

# Lire le fichier JSON
data <- fromJSON(json_file, simplifyDataFrame = FALSE)  # Lire comme une liste
print(str(data))  # Vérifier la structure de data

# Afficher les avertissements pour diagnostic
if (length(warnings()) > 0) {
  print(warnings())
}

# Étape 1 : Associer chaque centre de cluster à une cellule Voronoï
cluster_to_cell <- data.frame()
for (i in 1:nrow(cluster_centers)) {
  center_point <- cluster_centers[i, ]
  cluster_id <- cluster_centers$cluster_id[i]  # Ajuste si le champ est différent (ex. 'id')
  for (j in 1:nrow(voronoi_cells)) {
    if (st_contains(voronoi_cells[j, ], center_point, sparse = FALSE)) {
      cluster_to_cell <- rbind(cluster_to_cell, data.frame(cluster_id = cluster_id, cell_idx = j))
      break
    }
  }
}
print(cluster_to_cell)  # Vérifier l'association

# Étape 2 : Calculer les voisins par arête et par sommet
neighbors_by_edge <- setNames(lapply(unique(cluster_to_cell$cluster_id), function(cluster) character()), unique(cluster_to_cell$cluster_id))
neighbors_by_vertex <- setNames(lapply(unique(cluster_to_cell$cluster_id), function(cluster) character()), unique(cluster_to_cell$cluster_id))

# Voisinage par arête (cellules qui partagent une frontière)
for (i in 1:(nrow(voronoi_cells)-1)) {
  for (j in (i+1):nrow(voronoi_cells)) {
    if (st_touches(voronoi_cells[i, ], voronoi_cells[j, ], sparse = FALSE)) {
      cluster1 <- cluster_to_cell$cluster_id[cluster_to_cell$cell_idx == i]
      cluster2 <- cluster_to_cell$cluster_id[cluster_to_cell$cell_idx == j]
      if (length(cluster1) > 0 && length(cluster2) > 0) {
        neighbors_by_edge[[as.character(cluster1)]] <- c(neighbors_by_edge[[as.character(cluster1)]], as.character(cluster2))
        neighbors_by_edge[[as.character(cluster2)]] <- c(neighbors_by_edge[[as.character(cluster2)]], as.character(cluster1))
        cat(sprintf("Edge neighbor: Cluster %s <-> Cluster %s\n", cluster1, cluster2))
      }
    }
  }
}

# Voisinage par sommet (cellules qui se rencontrent à un sommet)
for (i in 1:(nrow(voronoi_cells)-1)) {
  cell1 <- voronoi_cells[i, ]
  cell1_vertices <- st_coordinates(st_cast(st_boundary(cell1), "POINT"))[, c("X", "Y")]
  for (j in (i+1):nrow(voronoi_cells)) {
    cell2 <- voronoi_cells[j, ]
    cell2_vertices <- st_coordinates(st_cast(st_boundary(cell2), "POINT"))[, c("X", "Y")]
    shared_vertices <- FALSE
    for (v1 in 1:nrow(cell1_vertices)) {
      for (v2 in 1:nrow(cell2_vertices)) {
        if (all(abs(cell1_vertices[v1, ] - cell2_vertices[v2, ]) < 1e-6)) {  # Tolérance pour les coordonnées
          shared_vertices <- TRUE
          break
        }
      }
      if (shared_vertices) break
    }
    if (shared_vertices) {
      cluster1 <- cluster_to_cell$cluster_id[cluster_to_cell$cell_idx == i]
      cluster2 <- cluster_to_cell$cluster_id[cluster_to_cell$cell_idx == j]
      if (length(cluster1) > 0 && length(cluster2) > 0 && !as.character(cluster2) %in% neighbors_by_edge[[as.character(cluster1)]]) {
        neighbors_by_vertex[[as.character(cluster1)]] <- c(neighbors_by_vertex[[as.character(cluster1)]], as.character(cluster2))
        neighbors_by_vertex[[as.character(cluster2)]] <- c(neighbors_by_vertex[[as.character(cluster2)]], as.character(cluster1))
        cat(sprintf("Vertex neighbor: Cluster %s <-> Cluster %s\n", cluster1, cluster2))
      }
    }
  }
}

# Combiner les voisins (arête + sommet) et supprimer les doublons
all_neighbors <- lapply(names(neighbors_by_edge), function(cluster) {
  unique(c(neighbors_by_edge[[cluster]], neighbors_by_vertex[[cluster]]))
})
names(all_neighbors) <- names(neighbors_by_edge)

# Vérifier les voisins générés
print(all_neighbors)

# Étape 3 : Ajouter le champ neighbors à chaque document
for (i in 1:length(data)) {
  doc <- data[[i]]
  cluster_id <- as.character(doc$cluster)
  if (!is.null(cluster_id) && cluster_id %in% names(all_neighbors)) {
    doc$neighbors <- all_neighbors[[cluster_id]]
  }
  
  # Gérer le champ _id avec un identifiant unique
  if (is.null(doc$`_id`)) {
    doc$`_id` <- sprintf("oid_%04d", i)  # Générer un ID unique
  } else if (is.list(doc$`_id`) && !is.null(doc$`_id`$oid)) {
    doc$`_id` <- doc$`_id`$oid  # Extraire la valeur $oid
  }
  
  # Mettre à jour data avec le document modifié
  data[[i]] <- doc
  
  # Remplacer complètement le document dans MongoDB
  mongo$replace(sprintf('{"_id": "%s"}', doc$`_id`), toJSON(doc, auto_unbox = TRUE))
}

# Étape 4 : Créer les index
mongo$index(add = '{"neighbors": 1}')
cat("Index sur 'neighbors' créé avec succès.\n")
# Pour la Possibilité 1 : ajouter un index 2dsphere
mongo$index(add = '{"location": "2dsphere"}')
cat("Index 2dsphere sur 'location' créé avec succès.\n")

# Sauvegarder le fichier JSON mis à jour
write_json(data, "C:/Users/ZINA KARIM/python_projet/kcluster/ouaga_with_clusters_updated.json", pretty = TRUE, auto_unbox = TRUE)

# Vérification
cat("Exemple de document mis à jour :\n")
print(mongo$find(limit = 1))