# main.py

import sys
import os

# Ajout du dossier courant au path Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ui.main_window import ProtocoleGUI
from PySide6.QtWidgets import QApplication
from core.utils import get_base_dir  # Assure-toi que cette fonction existe bien

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")  # ← désactivé comme demandé

    # Charger le style global depuis resources/style.qss
    style_path = os.path.join(get_base_dir(), "resources", "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print("❌ Fichier style.qss introuvable :", style_path)

    window = ProtocoleGUI()
    window.show()
    sys.exit(app.exec())
