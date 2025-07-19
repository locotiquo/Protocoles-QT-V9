import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QListWidget, QTextEdit, QSplitter
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class FichesPratiquesTab(QWidget):
    def __init__(self, base_dir):
        super().__init__()

        self.base_dir = base_dir
        self.data_path = os.path.join(base_dir, "resources", "fiches_pratiques.json")

        self.init_ui()
        self.charger_donnees()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher un motif…")
        self.search_bar.textChanged.connect(self.filtrer_motifs)
        layout.addWidget(self.search_bar)

        self.splitter = QSplitter(Qt.Horizontal)

        self.liste_motifs = QListWidget()
        self.liste_motifs.itemClicked.connect(self.afficher_fiche)
        self.splitter.addWidget(self.liste_motifs)

        self.zone_affichage = QTextEdit()
        self.zone_affichage.setReadOnly(True)
        self.splitter.addWidget(self.zone_affichage)

        layout.addWidget(self.splitter)

    def charger_donnees(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.donnees = json.load(f)
        except Exception as e:
            self.donnees = []
            self.zone_affichage.setPlainText(f"Erreur lors du chargement des données : {e}")
            return

        self.motifs_originaux = [item["motif"] for item in self.donnees]
        self.liste_motifs.addItems(self.motifs_originaux)

    def filtrer_motifs(self, texte):
        texte = texte.strip().lower()
        self.liste_motifs.clear()

        for item in self.donnees:
            if texte in item["motif"].lower():
                self.liste_motifs.addItem(item["motif"])

    def afficher_fiche(self, item):
        motif_choisi = item.text()
        fiche = next((f for f in self.donnees if f["motif"] == motif_choisi), None)

        if fiche:
            texte = f"<h2>{fiche['motif']}</h2>"

            if fiche.get("questions"):
                texte += "<b>Questions à poser :</b><ul>"
                for question in fiche["questions"]:
                    texte += f"<li>{question}</li>"
                texte += "</ul>"

            if fiche.get("signes_alerte"):
                texte += "<b>Signes d’alerte :</b><ul>"
                for signe in fiche["signes_alerte"]:
                    texte += f"<li>{signe}</li>"
                texte += "</ul>"

            self.zone_affichage.setHtml(texte)
        else:
            self.zone_affichage.setPlainText("Fiche non trouvée.")
