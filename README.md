## 🇬🇧 English version

# 🛰️ Scalable Spatial Data Processing and Geospatial Index Optimization

## 📌 Overview

This project presents a comprehensive and scalable framework for **spatial data processing**, **clustering**, and **geospatial query optimization** using real-world data collected in Ouagadougou (Burkina Faso).

🎯 The main objective is to improve query performance in **geospatial NoSQL databases** by combining advanced spatial modeling and indexing strategies.

🔗 **Full manuscript (detailed methodology and results):**  
https://drive.google.com/file/d/1K6SgNbvxBHv69hW-h2tSLjJiX3o0-P30/view?usp=sharing

---

## 🚀 Core Contributions

✔ Hybrid spatial modeling (Voronoi + Regular Grid)  
✔ Novel neighborhood-based indexing strategy  
✔ Performance evaluation of geospatial queries in MongoDB  
✔ Integration of sequential and distributed processing (Spark)  
✔ Scalable approach for large spatial datasets  

---

## 🗂️ Data Preparation

Initial data were collected from field surveys and stored in:

* `Ouagadougou.xlsx`

Data conversion pipeline:

* Excel → JSON using Python (`pandas`)
* Script: `ConversionXLSX_toJSON.py`

Each document includes:

- Enterprise information  
- Product type  
- GPS coordinates  
- Administrative attributes  

---

## 🧠 Approach 1: Voronoi-Based Spatial Modeling

### 🔹 Methodology

- K-means clustering  
- Voronoi diagram generation (R – `deldir`)  
- Cluster assignment  
- Spatial export for GIS visualization  

### 📁 Key Files

- `Enrichi_En_cluster_JSON_to_Mongo_shp_TO_Qgis.R`  
- `Enrichi_En_voisinage.R`  
- `ouaga_with_clusters.json`  
- `ouaga_with_clusters_updated.json`  

### 📊 Outputs

- Clustered spatial data  
- Neighbor relationships  
- GIS layers:

  - `entreprises_points.shp`  
  - `voronoi_cells.shp`  
  - `centroids.shp`  

---

## ⚡ Performance Evaluation (Voronoi Approach)

### Indexes Tested

- `_id` (default)  
- `location_2dsphere`  
- `neighbors_1`  
- `cluster_1_neighbors_1`  

### 📈 Key Insight

👉 Neighborhood-based indexes significantly outperform purely spatial indexes in query efficiency.

---

## 🧩 Approach 2: Regular Grid-Based Modeling

### 🔹 Methodology

- Grid generation (7 km × 7 km)  
- Cluster assignment  
- Correction of unassigned points  
- 8-neighborhood computation  

### 📁 Key Files

- `Enrichie_cluster_shpToQgis.R`  
- `Enrichie_cluster_surLigne_shpToQgis.R`  
- `Enrichie_cluster_voisin.R`  

### 📊 Outputs

- `ouaga_cluster.json`  
- `ouaga_cluster_corrige.json`  
- `ouaga_cluster_voisins.json`  

---

## ⚡ Performance Evaluation (Grid Approach)

### Indexes Tested

- `cluster_1`  
- `voisins_1`  
- `localisation_site_2dsphere`  

### 📈 Key Insight

- Cluster and neighborhood indexes are the most efficient  
- `COLLSCAN` is the least efficient (full scan)  

---

## 🔍 Advanced Algorithm: Progressive Cluster Selection

This project introduces a spatial selection algorithm based on:

➡️ **Analytical Discrete Circle (Eric Andres)**

### 🎯 Objective

- Progressive expansion of spatial search radius  
- Efficient selection of relevant clusters  

### 📁 Files

- `eric9.py` (Voronoi)  
- `eric8.py` (Grid)  

### 📊 Outputs

- `selected_cells.geojson`  
- `selected_cells.shp`  

---

## ⚙️ Sequential vs Parallel Processing

### 🔹 Sequential Processing

- Python + PyMongo  
- Files: `seq*.py`  

### 🔹 Distributed Processing

- Apache Spark (PySpark)  
- Files: `spark*.py`  

### 📈 Key Insight

👉 Parallel processing significantly improves performance for large-scale spatial data.

---

## 🧰 Technologies

- Python (Pandas, PyMongo)  
- R (Spatial computation)  
- MongoDB (Geospatial indexing)  
- QGIS (Visualization)  
- Apache Spark (Distributed computing)  

---

## 🌍 Impact & Applications

This work contributes to:

- Smart city infrastructure  
- Urban planning optimization  
- Spatial decision support systems  
- Large-scale geospatial analytics  

---

## 📚 Publications

🔗 Full list (ORCID):  
https://orcid.org/0009-0009-2775-8405

---

### 1. Classification of Spatial Data Based on K-means and Voronoi Diagram

KABORE M., et al. (2024)  
International Journal of Advanced Computer Science and Applications (IJACSA)

🔗 DOI: https://doi.org/10.14569/IJACSA.2024.01507139  

💡 Related code available in this repository  

---

### 2. A Framework for Data Research in GIS Database using Meshing Techniques and MapReduce

SERE A., OUATTARA J.S.D., et al., KABORE M. (2021)  
IJACSA  

🔗 DOI: https://doi.org/10.14569/IJACSA.2021.0120374  

---

### 3. Data Search in Smart GIS Database using MapReduce Pattern and Bayesian Probability

KABORE M., et al. (2025)  
Springer – ICICT  
https://drive.google.com/file/d/1rghrzPdZQC4AO5d6YQFV1PPl_jBXcG8P/view?usp=sharing

🔗 DOI: https://doi.org/10.1007/978-981-96-6435-1_24  

---

### 4. Search Algorithms in Large Spatial Data using Analytical Digital Circle

KABORE M., et al. (2025)  
Springer  

🔗 DOI: https://doi.org/10.1007/978-3-032-11521-8_9  

💡 Related code: OpenMP + spatial search  

---

### 5. Improving the Architecture of Expert Systems for GIS Data Search

ZOUNGRANA B.O.I., KABORE M., et al. (2025)

🔗 DOI: https://doi.org/10.1109/ACDSA65407.2025.11166159  

🟡 Work in Progress

Applied Spatial Data Classification Using K-means and Voronoi Diagram: A Case Study
KABORE M., et al. (2025)
👉 Accepted – extension of the 2024 model

## 📬 Author

**Moubaric KABORE**  
PhD in Computer Science – Data Science  

🔬 Spatial Data Science | GIS | Big Data | Distributed Systems  

---

## 🔮 Future Work

- Real-time spatial data integration  
- AI-based geospatial prediction  
- Smart city decision systems  
- Distributed spatial indexing at scale

...

## 🇫🇷 Version française

# 🛰️ Traitement Spatial Scalable et Optimisation des Index Géospatiaux

## 📌 Vue d’ensemble

Ce projet propose un cadre complet et scalable pour le **traitement des données spatiales**, le **clustering**, et l’**optimisation des requêtes géospatiales**, basé sur des données réelles collectées à Ouagadougou (Burkina Faso).

🎯 L’objectif principal est d’améliorer les performances des requêtes dans les **bases de données NoSQL géospatiales** en combinant des techniques avancées de modélisation spatiale et d’indexation.

🔗 **Manuscrit complet (méthodologie détaillée et résultats) :**  
https://drive.google.com/file/d/1K6SgNbvxBHv69hW-h2tSLjJiX3o0-P30/view?usp=sharing

---

## 🚀 Contributions principales

✔ Modélisation spatiale hybride (Voronoï + grille régulière)  
✔ Nouvelle stratégie d’indexation basée sur le voisinage  
✔ Évaluation des performances des requêtes géospatiales sous MongoDB  
✔ Intégration de traitements séquentiels et distribués (Spark)  
✔ Approche scalable pour les grandes bases de données spatiales  

---

## 🗂️ Préparation des données

Les données initiales ont été collectées sur le terrain et stockées dans :

* `Ouagadougou.xlsx`

Pipeline de transformation :

* Excel → JSON avec Python (`pandas`)  
* Script : `ConversionXLSX_toJSON.py`

Chaque document contient :

- Informations sur l’entreprise  
- Type de produit  
- Coordonnées GPS  
- Données administratives  

---

## 🧠 Approche 1 : Modélisation spatiale basée sur Voronoï

### 🔹 Méthodologie

- Clustering K-means  
- Génération de diagrammes de Voronoï (R – `deldir`)  
- Affectation des points aux clusters  
- Export des données pour visualisation SIG  

### 📁 Fichiers principaux

- `Enrichi_En_cluster_JSON_to_Mongo_shp_TO_Qgis.R`  
- `Enrichi_En_voisinage.R`  
- `ouaga_with_clusters.json`  
- `ouaga_with_clusters_updated.json`  

### 📊 Résultats

- Données clusterisées  
- Relations de voisinage entre clusters  
- Couches SIG :

  - `entreprises_points.shp`  
  - `voronoi_cells.shp`  
  - `centroids.shp`  

---

## ⚡ Évaluation des performances (Approche Voronoï)

### Index testés

- `_id` (index par défaut)  
- `location_2dsphere`  
- `neighbors_1`  
- `cluster_1_neighbors_1`  

### 📈 Résultat clé

👉 Les index basés sur le voisinage surpassent significativement les index purement géospatiaux en termes de performance.

---

## 🧩 Approche 2 : Modélisation basée sur grille régulière

### 🔹 Méthodologie

- Génération de grilles carrées (7 km × 7 km)  
- Affectation des points aux cellules  
- Correction des points non assignés  
- Calcul du voisinage (8-voisinage)  

### 📁 Fichiers principaux

- `Enrichie_cluster_shpToQgis.R`  
- `Enrichie_cluster_surLigne_shpToQgis.R`  
- `Enrichie_cluster_voisin.R`  

### 📊 Résultats

- `ouaga_cluster.json`  
- `ouaga_cluster_corrige.json`  
- `ouaga_cluster_voisins.json`  

---

## ⚡ Évaluation des performances (Approche grille)

### Index testés

- `cluster_1`  
- `voisins_1`  
- `localisation_site_2dsphere`  

### 📈 Résultat clé

- Les index de cluster et de voisinage sont les plus performants  
- `COLLSCAN` est le moins performant (balayage complet)  

---

## 🔍 Algorithme avancé : Sélection progressive des clusters

Ce projet introduit un algorithme de sélection spatiale basé sur :

➡️ **le cercle discret analytique (Eric Andrès)**

### 🎯 Objectif

- Expansion progressive du rayon de recherche  
- Sélection efficace des clusters pertinents  

### 📁 Fichiers

- `eric9.py` (Voronoï)  
- `eric8.py` (Grille)  

### 📊 Résultats

- `selected_cells.geojson`  
- `selected_cells.shp`  

---

## ⚙️ Traitement séquentiel vs parallèle

### 🔹 Traitement séquentiel

- Python + PyMongo  
- Fichiers : `seq*.py`  

### 🔹 Traitement distribué

- Apache Spark (PySpark)  
- Fichiers : `spark*.py`  

### 📈 Résultat clé

👉 Le traitement parallèle améliore significativement les performances sur des données volumineuses.

---

## 🧰 Technologies utilisées

- Python (Pandas, PyMongo)  
- R (calcul spatial)  
- MongoDB (indexation géospatiale)  
- QGIS (visualisation)  
- Apache Spark (calcul distribué)  

---

## 🌍 Impact et applications

Ce travail contribue à :

- Les infrastructures de villes intelligentes  
- L’optimisation de la planification urbaine  
- Les systèmes d’aide à la décision spatiale  
- L’analyse géospatiale à grande échelle  

---

## 📚 Publications

🔗 Liste complète (ORCID) :  
https://orcid.org/0009-0009-2775-8405

---

### 1. Classification des données spatiales basée sur K-means et diagramme de Voronoï

KABORE M., et al. (2024)  
International Journal of Advanced Computer Science and Applications (IJACSA)

🔗 DOI : https://doi.org/10.14569/IJACSA.2024.01507139  

💡 Code associé disponible dans ce dépôt  

---

### 2. Framework de recherche de données dans une base SIG avec MapReduce

SERE A., et al., KABORE M. (2021)  
IJACSA  

🔗 DOI : https://doi.org/10.14569/IJACSA.2021.0120374  

---

### 3. Recherche de données dans les bases SIG avec MapReduce et probabilité bayésienne

KABORE M., et al. (2025)  
Springer – ICICT  

🔗 DOI : https://doi.org/10.1007/978-981-96-6435-1_24  

---

### 4. Algorithmes de recherche dans de grandes données spatiales via cercle discret analytique

KABORE M., et al. (2025)  
Springer  

🔗 DOI : https://doi.org/10.1007/978-3-032-11521-8_9  

💡 Code associé : OpenMP + recherche spatiale  

---

### 5. Amélioration de l’architecture des systèmes experts pour la recherche dans les bases SIG

ZOUNGRANA B.O.I., KABORE M., et al. (2025)

🔗 DOI : https://doi.org/10.1109/ACDSA65407.2025.11166159  

### 🟡 Travaux en cours

Application de la classification spatiale (2025)  
👉 Accépté - extension du modèle proposé en 2024  

## 📬 Auteur

**Moubaric KABORE**  
Doctorat en Informatique – Science des données  

🔬 Science des données spatiales | SIG | Big Data | Systèmes distribués  

---

## 🔮 Travaux futurs

- Intégration de données spatiales en temps réel  
- Modèles d’apprentissage automatique pour la prédiction spatiale  
- Systèmes intelligents d’aide à la décision urbaine  
- Indexation spatiale distribuée à grande échelle  
