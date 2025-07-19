from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget, QScrollArea
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import os

from core.utils import get_base_dir


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("À propos")
        self.setMinimumSize(650, 450)

        # 🔲 Layout principal
        layout = QVBoxLayout(self)

        # 🔠 Titre
        title_label = QLabel("Informations sur le logiciel")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label, alignment=Qt.AlignLeft)

        # 🖱️ ScrollArea pour contenu
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        scroll.setWidget(content_widget)
        content_layout = QHBoxLayout(content_widget)

        # 📷 Image à gauche
        img_path = os.path.join(get_base_dir(), "resources", "logo.png")
        image_label = QLabel()
        pixmap = QPixmap(img_path)
        image_label.setPixmap(pixmap.scaledToWidth(100, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignTop)
        image_label.setStyleSheet("margin-right: 15px;")
        content_layout.addWidget(image_label)

        # 📝 Texte à droite
        text = """
Ce logiciel est strictement destiné à un usage interne au SAMU 14.

Toute reproduction ou diffusion sans autorisation est interdite.

📜 Cadre légal :
- Ce programme n’a pas vocation à remplacer les outils réglementaires.
- Son usage doit respecter les protocoles de régulation médicale en vigueur.
- Ce programme se veut une aide aux ARM, et ne se substitue pas aux éléments cliniques reçus.

👤 Concepteur :
- Nom : Adrien Rost
- Contact : rost-a@chu-caen.fr

ℹ️ Version logiciel : 
- Protocoles en vigueur : V3

- Version : 8
    -modification interface, correction bugs mineurs

- Version : 7.5:
    -ajout d'un filtre dynamique sur l'onglet plateau caennais
    
- Version : 7
    - ajout onglet plateau technique Caennais

- Version : 6.1
    - Modif couleur P2
- Version : 6.0
    - Interface, menus, taille police, options d'affichage
"""
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setFont(QFont("Arial", 11))
        content_layout.addWidget(text_label)

        layout.addWidget(scroll)

        # 🔘 Bouton Fermer
        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)
