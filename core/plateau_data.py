# plateau_data.py
import csv
import os

def charger_plateau_donnees(fichier_csv):
    """
    Charge les données du fichier plateau.csv comme une liste de dictionnaires.
    Chaque dictionnaire correspond à une ligne avec des clés issues de l'en-tête.
    """
    if not os.path.exists(fichier_csv):
        raise FileNotFoundError(f"Fichier introuvable : {fichier_csv}")

    with open(fichier_csv, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)
