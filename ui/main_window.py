import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTreeView, QMenuBar,
    QHeaderView, QMessageBox, QAbstractItemView, QStyledItemDelegate, QStyle, QSizePolicy, QTabWidget
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QAction, QFont, QFontMetrics, QColor
from PySide6.QtCore import Qt, QPoint, QSize, QEvent, QTimer

from core.utils import supprimer_accents, extract_csv_if_frozen, get_base_dir, get_icon_path, recherche
from core.csv_loader import charger_csv
from core.image_loader import charger_image
from core.plateau_data import charger_plateau_donnees


from ui.tooltip import ToolTip
from ui.bilans_tab import BilansSimplifiesTab
from ui.help_dialog import HelpDialog
from ui.plateau_tab import PlateauCaennaisTab
from ui.fiches_pratiques_tab import FichesPratiquesTab
from ui.delegates import NoHoverDelegate, BilansTreeDelegate, ImageCenterDelegate
from ui.menus import creer_menus
from ui.main_window_ui import init_ui
from ui.filtrage import filtrer_motifs
from ui.main_window_utils import ajuster_largeur_colonnes, ajuster_taille_fenetre
from ui.font_utils import appliquer_taille_police, afficher_etat_options


class ProtocoleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_dir = get_base_dir()
        self.csv_path = extract_csv_if_frozen()
        self.df = charger_csv(self.csv_path)

        self.plateau_path = os.path.join(self.base_dir, "resources", "plateau.csv")
        self.plateau_data = charger_plateau_donnees(self.plateau_path)


        self.setWindowTitle("Protocoles QT")
        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.col_widths = []
        self.taille_police = 12

        self.status_bar = self.statusBar()

        # Message temporaire à gauche
        self.status_left_label = QLabel("Prêt")
        self.status_bar.addWidget(self.status_left_label)

        # Message permanent à droite
        self.status_right_label = QLabel()
        self.status_right_label.setStyleSheet("font-weight: bold; color: #555;")
        self.status_bar.addPermanentWidget(self.status_right_label)

        self.filtrer_motifs = lambda: filtrer_motifs(self)

        self.ajuster_largeur_colonnes = lambda: ajuster_largeur_colonnes(self)
        self.ajuster_taille_fenetre = lambda nb: ajuster_taille_fenetre(self, nb)

        self.appliquer_taille_police = lambda sender=None: appliquer_taille_police(self, sender)

        self.afficher_etat_options = lambda: afficher_etat_options(self)


        self.init_ui()

        self.afficher_etat_options()

        self.plateau_tab.set_font_size(self.taille_police)  # 👈 ligne importante


    
    def init_ui(self):
        init_ui(self)


    def onglet_change(self, index):
        nom = self.tabs.tabText(index)
        self.status_left_label.setText(f"Onglet actif : {nom}")
        QTimer.singleShot(3000, lambda: self.status_left_label.setText("Prêt"))
      

    def option_changee(self, action):
        filtrer_motifs(self)
        etat = "activée" if action.isChecked() else "désactivée"
        self.status_bar.showMessage(f"{action.text()} {etat}", 3000)


    def effacer_recherche(self):
        self.entry.clear()
  

    def ouvrir_fenetre_info(self):
        dlg = HelpDialog(self)
        dlg.exec()


    from PySide6.QtCore import QEvent

    def eventFilter(self, source, event):
        # Tooltip pour le tree principal
        if source == self.tree.viewport():
            if event.type() == QEvent.MouseMove:
                index = self.tree.indexAt(event.position().toPoint())
                if index.isValid():
                    data = self.model.data(index)
                    if data:
                        pos = self.tree.mapToGlobal(event.position().toPoint() + QPoint(20, 10))
                        self.tooltip.show_tooltip(str(data), pos.x(), pos.y())
                        return True
                self.tooltip.hide()
            elif event.type() == QEvent.Leave:
                self.tooltip.hide()

        # Tooltip pour tree_bs (bilans)
        if hasattr(self, "bilans_tab") and source == self.bilans_tab.tree_bs.viewport():
            if event.type() in (QEvent.MouseMove, QEvent.HoverMove):  # ✅ ajout HoverMove
                pos = event.position().toPoint()
                index = self.bilans_tab.tree_bs.indexAt(pos)
                if index.isValid():
                    data = self.bilans_tab.model.data(index)
                    if data:
                        pos_global = self.bilans_tab.tree_bs.mapToGlobal(pos + QPoint(20, 10))
                        self.tooltip.show_tooltip(str(data), pos_global.x(), pos_global.y())
                        return True
                self.tooltip.hide()
            elif event.type() == QEvent.Leave:
                self.tooltip.hide()

        # Esc pour effacer
        if source == self.entry and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.entry.clear()
                return True

        return super().eventFilter(source, event)





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ProtocoleGUI()
    window.show()
    sys.exit(app.exec())