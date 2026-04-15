import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import os

# ===================== DOSSIER DE SORTIE =====================
output_dir = r"F:\G_regul_G_irregul\python_projet\Grille_Regul"
os.makedirs(output_dir, exist_ok=True)   # Crée le dossier s'il n'existe pas

# === PARAMÈTRES ===
grid_shp_path = "C:/Users/ZINA KARIM/python_projet/autre/ouaga_grille_clusters.shp"

center = (12.37, -1.52)   # (lat, lon)
radius = 0.05             # rayon du cercle

# === LECTURE DE LA GRILLE ===
grid_gdf = gpd.read_file(grid_shp_path)
print(f"Grille chargée : {len(grid_gdf)} cellules, CRS : {grid_gdf.crs}")

if grid_gdf.crs is None or grid_gdf.crs.to_string() != 'EPSG:4326':
    grid_gdf = grid_gdf.to_crs(epsg=4326)
    print("CRS converti en WGS84 (EPSG:4326)")

# === CRÉATION DU CERCLE ===
center_point = Point(center[1], center[0])
circle = center_point.buffer(radius)

# === SÉLECTION DES CELLULES ===
grid_gdf['selected'] = grid_gdf.geometry.intersects(circle)
selected_cells = grid_gdf[grid_gdf['selected'] == True].copy()

print(f"Cellules sélectionnées par le cercle : {len(selected_cells)}")

if len(selected_cells) == 0:
    print("⚠️  Aucune cellule sélectionnée. Essayez d'augmenter le rayon.")

# === EXPORT DANS LE DOSSIER DEMANDÉ ===
output_geojson = os.path.join(output_dir, "selected_cells2.geojson")
selected_cells.to_file(output_geojson, driver='GeoJSON')
print(f"✅ GeoJSON créé : {output_geojson}")

output_shp = os.path.join(output_dir, "selected_cells2.shp")
selected_cells.to_file(output_shp)
print(f"✅ Shapefile créé : {output_shp}")

print(f"\nLes fichiers sont maintenant dans : {output_dir}")

# === VISUALISATION ===
fig, ax = plt.subplots(figsize=(10, 8))
grid_gdf.plot(ax=ax, color='lightgray', alpha=0.5, edgecolor='gray', linewidth=0.3)

if len(selected_cells) > 0:
    selected_cells.plot(ax=ax, color='red', alpha=0.4, edgecolor='darkred', linewidth=0.8)

circle_gdf = gpd.GeoDataFrame([1], geometry=[circle], crs='EPSG:4326')
circle_gdf.boundary.plot(ax=ax, color='red', linewidth=2)

ax.scatter(center[1], center[0], color='blue', s=100, label='Personne (centre)')
ax.set_aspect('equal')
ax.set_title("Superposition du cercle d'Eric Andres sur la grille régulière")
ax.legend()
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()