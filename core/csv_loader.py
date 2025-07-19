# csv_loader.py
import csv

def charger_csv(fichier):
    """
    Charge le fichier CSV en liste de dictionnaires.
    Le CSV est attendu en UTF-8 BOM (utf-8-sig) et séparé par des points-virgules.
    """
    with open(fichier, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)
