import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# === PARAMÈTRES ===
# Chemin vers ton fichier Shapefile de la grille
grid_shp_path = "F:/G_regul_G_irregul/python_projet/Grille_Irregul/voronoi_cells.shp" # Remplace par ton chemin réel !

# Position de la personne (au centre d'Ouaga)
center = (12.37, -1.6141)  # (lat, lon)
radius = 0.04  # rayon du cercle (~2 km) en degrés

# === LECTURE DE TA GRILLE ===
grid_gdf = gpd.read_file(grid_shp_path)
print(f"Grille chargée : {len(grid_gdf)} cellules, CRS : {grid_gdf.crs}")

# Vérif/force le CRS en WGS84 si besoin
if grid_gdf.crs is None:
    grid_gdf.set_crs(epsg=4326, inplace=True)
elif grid_gdf.crs != 'EPSG:4326':
    grid_gdf.to_crs(epsg=4326, inplace=True)
    print("CRS converti en WGS84 (EPSG:4326)")

# === CRÉATION DU CERCLE ===
center_point = Point(center[1], center[0])  # (lon, lat) pour Shapely
circle = center_point.buffer(radius)

# === SUPERPOSITION : SÉLECTION DES CELLULES INTERSECTÉES ===
# Ajoute une colonne pour marquer les cellules sélectionnées
grid_gdf['selected'] = grid_gdf.geometry.intersects(circle)
selected_cells = grid_gdf[grid_gdf['selected'] == True].copy()

print(f"Cellules sélectionnées par le cercle : {len(selected_cells)}")

# === EXPORT POUR QGIS / PARTAGE ===
output_shp = 'selected_cells.shp'  # Nouveau Shapefile des cellules allumées
selected_cells.to_file(output_shp)
print(f"Export réussi vers '{output_shp}' ! Importe-le dans QGIS pour superposer.")

# Optionnel : Export GeoJSON aussi (plus léger)
selected_cells.to_file('selected_cells.geojson', driver='GeoJSON')
print("Export GeoJSON aussi : 'selected_cells.geojson'")

# === VISUALISATION RAPIDE (optionnelle) ===
fig, ax = plt.subplots(figsize=(10, 8))
# Toute la grille en gris clair
grid_gdf.plot(ax=ax, color='lightgray', alpha=0.5, edgecolor='gray', linewidth=0.3)
# Cellules sélectionnées en rouge
selected_cells.plot(ax=ax, color='red', alpha=0.3, edgecolor='darkred', linewidth=0.5)
# Cercle en rouge foncé
circle_gdf = gpd.GeoDataFrame([1], geometry=[circle], crs='EPSG:4326')
circle_gdf.boundary.plot(ax=ax, color='red', linewidth=2)
# Centre en bleu
ax.scatter(center[1], center[0], color='blue', s=100, label='Personne (centre)')
ax.set_aspect('equal')
ax.set_title("Superposition du cercle d'Eric Andres sur la grille couvrant la ville de Ouagadougou", fontsize=13)
ax.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()