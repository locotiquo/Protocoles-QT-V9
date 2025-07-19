# utils.py
import os
import sys
import unicodedata
import tempfile
import shutil

def supprimer_accents(texte):
    """Supprime les accents d’une chaîne de caractères."""
    return unicodedata.normalize('NFD', texte).encode('ascii', 'ignore').decode('utf-8')

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def get_csv_path():
    """
    Retourne le chemin du CSV dans le répertoire resources.
    """
    return os.path.join(get_base_dir(), "resources", "Protocoles_de_regulation.csv")

def get_icon_path():
    """
    Retourne le chemin vers le fichier logo.ico dans le répertoire resources.
    """
    return os.path.join(get_base_dir(), "resources", "logo.ico")

def extract_csv_if_frozen():
    """
    Si l'application est gelée (PyInstaller onefile),
    copie le CSV dans le dossier temporaire (lecture autorisée), sinon retourne le chemin direct.
    """
    if getattr(sys, 'frozen', False):
        temp_dir = tempfile.gettempdir()
        temp_csv_path = os.path.join(temp_dir, "Protocoles_de_regulation.csv")
        if not os.path.exists(temp_csv_path):
            shutil.copy(get_csv_path(), temp_csv_path)
        return temp_csv_path
    else:
        return get_csv_path()

def recherche(texte_recherche, liste):
    """
    Retourne les éléments de `liste` contenant `texte_recherche` (sans accents, insensible à la casse).
    """
    texte_filtre = supprimer_accents(texte_recherche).lower()
    return [item for item in liste if texte_filtre in supprimer_accents(item).lower()]
