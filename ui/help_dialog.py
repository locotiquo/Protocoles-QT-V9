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
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout(self)

        # Titre principal
        title_label = QLabel("Protocoles QT - Informations sur le logiciel")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # ScrollArea pour contenu
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        content_widget = QWidget()
        scroll.setWidget(content_widget)
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(20)

        # Image à gauche
        img_path = os.path.join(get_base_dir(), "resources", "logo.png")
        image_label = QLabel()
        pixmap = QPixmap(img_path)
        image_label.setPixmap(pixmap.scaledToWidth(120, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignTop)
        content_layout.addWidget(image_label)

        # Texte à droite avec HTML pour mise en forme
        text = """
<h3>Usage :</h3>
<p>Logiciel strictement destiné à un usage interne au SAMU 14.</p>

<h3>Cadre légal :</h3>
<ul>
<li>Ne remplace pas les outils réglementaires.</li>
<li>Respecter les protocoles de régulation médicale.</li>
<li>Aide à la régulation médicale, ne se substitue pas aux éléments cliniques.</li>
</ul>

<h3>Concepteur :</h3>
<p>Adrien Rost<br>rost-a@chu-caen.fr</p>

<h3>Protocoles en vigueur : V3</h3>

<h3>Version logiciel :</h3>
<ul>
<li>Version 9 : ajout raccourcis clavier</li>
<li>Version 8 : modification interface, correction bugs mineurs</li>
<li>Version 7.5 : ajout filtre dynamique sur l'onglet plateau Caennais</li>
<li>Version 7 : ajout onglet plateau technique Caennais</li>
<li>Version 6.1 : modification couleur P2</li>
<li>Version 6.0 : interface, menus, taille police, options d'affichage</li>
</ul>
"""
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setFont(QFont("Arial", 11))
        content_layout.addWidget(text_label)

        # Bouton fermer
        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)

