# onglets.py
from PySide6.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from ui.bilans_tab import BilansSimplifiesTab

class OngletsWidget(QTabWidget):
    def __init__(self, recherche_widget: QWidget, parent=None):
        super().__init__(parent)

        # Onglet 1 : Recherche de motifs
        self.addTab(recherche_widget, "Recherche de motifs")

        # Onglet 2 : Bilans simplifiés
        self.bs_tab = BilansSimplifiesTab()
        self.addTab(self.bs_tab, "Bilans simplifiés")
