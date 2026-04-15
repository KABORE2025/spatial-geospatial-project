import pandas as pd
import json
import os

def excel_to_json(excel_file_path, output_json_path):
    """
    Convertit un fichier Excel contenant des données d'entreprises de vente de véhicules en JSON.
    Args:
        excel_file_path (str): Chemin du fichier Excel.
        output_json_path (str): Chemin du fichier JSON de sortie.
    """
    try:
        # Vérifier si le fichier Excel existe
        if not os.path.exists(excel_file_path):
            raise FileNotFoundError(f"Le fichier {excel_file_path} n'existe pas.")

        # Lire le fichier Excel avec pandas
        print(f"Lecture du fichier Excel : {excel_file_path}")
        df = pd.read_excel(excel_file_path)

        # Vérifier les colonnes attendues
        expected_columns = ['Nom_entreprise', 'Type_marque', 'Quantite', 'Ville', 'Arrondissement', 'Secteur', 'latitude', 'longitude']
        for col in expected_columns:
            if col not in df.columns:
                raise ValueError(f"La colonne '{col}' est absente du fichier Excel.")

        # Nettoyage des données
        df = df.dropna(subset=expected_columns)  # Supprimer les lignes avec des valeurs manquantes dans les colonnes clés
        df = df.reset_index(drop=True)  # Réindexer après suppression

        # Validation des coordonnées pour le Burkina Faso
        df = df[
            (df['latitude'].between(9.5, 15.0)) &  # Latitude entre 9.5° et 15.0°
            (df['longitude'].between(-5.5, 2.5))   # Longitude entre -5.5° et 2.5°
        ]

        if df.empty:
            raise ValueError("Aucune donnée valide après validation des coordonnées.")

        # Créer une liste de dictionnaires pour le JSON
        data = []
        for index, row in df.iterrows():
            # Construire la structure du document
            doc = {
                "nom_entreprise": str(row['Nom_entreprise']),
                "type_marque": str(row['Type_marque']),
                "quantite": int(row['Quantite']),
                "ville": str(row['Ville']),
                "arrondissement": str(row['Arrondissement']),
                "secteur": str(row['Secteur']),
                "localisation_site": {
                    "coordinates": [float(row['longitude']), float(row['latitude'])]
                }
            }
            data.append(doc)

        # Écrire les données dans un fichier JSON
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Fichier JSON généré avec succès : {output_json_path}")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Chemins des fichiers
    excel_file_path = "C:/Users/ZINA KARIM/python_projet/Ouagadougou.xlsx"   # Remplace par ton chemin
    output_json_path = "C:/Users/ZINA KARIM/python_projet/autre/ouaga.json"  # Chemin de sortie

    # Appeler la fonction
    excel_to_json(excel_file_path, output_json_path)