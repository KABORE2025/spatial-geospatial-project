# 🛰️ Spatial Data Processing and Geospatial Index Optimization

## 📌 Overview

This project presents a comprehensive framework for **spatial data processing**, **clustering**, and **geospatial query optimization** using real-world data collected in Ouagadougou (Burkina Faso).

The objective is to improve query performance in **geospatial databases** by integrating:

* Spatial clustering (K-means)
* Voronoi diagram modeling
* Regular grid partitioning
* Neighborhood-based indexing
* Parallel and sequential data processing

---

## 🗂️ Data Preparation

Initial data were collected from field surveys and stored in an Excel file:

* `Ouagadougou.xlsx`

The data were converted into JSON format using Python (`pandas`):

* `ConversionXLSX_toJSON.py`

Each document contains attributes such as:

* Enterprise name
* Product type
* Location (GPS coordinates)
* Administrative information

---

## 🧠 Approach 1: Voronoi-Based Spatial Modeling

### 🔹 Steps

* Apply **K-means clustering**
* Generate **Voronoi diagrams** using R (`deldir`)
* Assign each point to a cluster
* Export spatial data for visualization in QGIS

### 📁 Key Files

* `Enrichi_En_cluster_JSON_to_Mongo_shp_TO_Qgis.R`
* `Enrichi_En_voisinage.R`
* `ouaga_with_clusters.json`
* `ouaga_with_clusters_updated.json`

### 📊 Output

* Clustered data
* Neighbor relationships between clusters
* Shapefiles for GIS visualization:

  * `entreprises_points.shp`
  * `voronoi_cells.shp`
  * `centroids.shp`

---

## ⚡ Performance Evaluation (Voronoi Approach)

Different indexes were tested in MongoDB:

* `_id` (default index)
* `location_2dsphere`
* `neighbors_1`
* `cluster_1_neighbors_1`

### 📈 Key Result

👉 Neighborhood-based indexes significantly outperform spatial-only indexes.

---

## 🧩 Approach 2: Regular Grid-Based Modeling

### 🔹 Steps

* Generate square grids (7 km × 7 km)
* Assign points to grid cells (clusters)
* Correct unassigned points
* Compute neighborhood (8-neighborhood)

### 📁 Key Files

* `Enrichie_cluster_shpToQgis.R`
* `Enrichie_cluster_surLigne_shpToQgis.R`
* `Enrichie_cluster_voisin.R`

### 📊 Output

* `ouaga_cluster.json`
* `ouaga_cluster_corrige.json`
* `ouaga_cluster_voisins.json`

---

## ⚡ Performance Evaluation (Grid Approach)

### Indexes Tested:

* `cluster_1`
* `voisins_1`
* `localisation_site_2dsphere`

### 📈 Key Result

* **Cluster and neighborhood indexes are the most efficient**
* `COLLSCAN` is the least efficient (full database scan)

---

## 🔍 Advanced Algorithm: Progressive Cluster Selection

We implement a spatial selection algorithm based on:

➡️ Analytical discrete circle (Eric Andres)

### 🎯 Objective

* Iteratively expand search radius
* Select relevant spatial clusters efficiently

### 📁 Files

* `eric9.py` (Voronoi)
* `eric8.py` (Grid)

### 📊 Output

* `selected_cells.geojson`
* `selected_cells.shp`

---

## ⚙️ Sequential vs Parallel Processing

Two processing strategies were implemented:

### 🔹 Sequential

* Python + PyMongo
* Files: `seq1`, `seq3`, `seq4`, etc.

### 🔹 Parallel

* Apache Spark (PySpark)
* Files: `spark3.py`, `spark4.py`, etc.

### 📈 Result

👉 Parallel processing significantly improves performance on large datasets.

---

## 🧰 Technologies Used

* Python (Pandas, PyMongo)
* R (Spatial processing)
* MongoDB (NoSQL, Geospatial indexing)
* QGIS (Visualization)
* Apache Spark (Big Data processing)

---

## 🎯 Key Contributions

✔ Hybrid spatial modeling (Voronoi + Grid)
✔ Neighborhood-based indexing strategy
✔ Performance evaluation of geospatial queries
✔ Scalable spatial data processing

---

## 📬 Author

**Moubaric KABORE**
PhD in Computer Science – Data Science
Spatial Data Science | GIS | Big Data

---

## 🔗 Future Work

* Integration with real-time urban systems
* Smart city applications
* AI-based spatial prediction

---
