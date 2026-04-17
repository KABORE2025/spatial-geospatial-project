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
