import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTreeView, QMenuBar,
    QHeaderView, QMessageBox, QAbstractItemView, QStyledItemDelegate, QStyle, QSizePolicy, QTabWidget
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QAction, QFont, QFontMetrics, QColor, QKeySequence, QShortcut
from PySide6.QtCore import Qt, QPoint, QSize, QEvent, QTimer

from core.utils import supprimer_accents, extract_csv_if_frozen, get_base_dir, get_icon_path, recherche
from core.csv_loader import charger_csv
from core.image_loader import charger_image
from core.plateau_data import charger_plateau_donnees


from ui.tooltip import ToolTip
from ui.bilans_tab import BilansSimplifiesTab
from ui.help_dialog import HelpDialog
from ui.plateau_tab import PlateauCaennaisTab





class NoHoverDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.state &= ~QStyle.State_MouseOver
        super().paint(painter, option, index)

class BilansTreeDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.state &= ~QStyle.State_MouseOver  # Désactive surbrillance au survol
        super().paint(painter, option, index)


class ImageCenterDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        else:
            background_brush = index.data(Qt.BackgroundRole)
            if background_brush:
                painter.fillRect(option.rect, background_brush)

        icon = index.data(Qt.DecorationRole)
        if isinstance(icon, QIcon):
            rect = option.rect
            pixmap = icon.pixmap(30, 30)
            x = rect.x() + (rect.width() - pixmap.width()) // 2
            y = rect.y() + (rect.height() - pixmap.height()) // 2
            painter.drawPixmap(x, y, pixmap)
        else:
            super().paint(painter, option, index)

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



        self.init_ui()

        self.afficher_etat_options()

        self.plateau_tab.set_font_size(self.taille_police)  # 👈 ligne importante


    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Onglet principal
        main_tab = QWidget()
        self.tabs.addTab(main_tab, "Recherche")
        main_tab_layout = QVBoxLayout(main_tab)

        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        fichier_menu = self.menu_bar.addMenu("Fichier")
        fichier_menu.addAction("Effacer la recherche", self.effacer_recherche)
        fichier_menu.addSeparator()
        fichier_menu.addAction("Quitter", self.close)

        options_menu = self.menu_bar.addMenu("Options")
        self.afficher_couleurs = QAction("Afficher les couleurs", self, checkable=True, checked=True)
        self.afficher_images = QAction("Afficher les images", self, checkable=True, checked=True)
        self.afficher_mise_en_forme = QAction("Afficher la mise en forme police", self, checkable=True, checked=True)
        for a in [self.afficher_couleurs, self.afficher_images, self.afficher_mise_en_forme]:
            a.triggered.connect(self.filtrer_motifs)
            a.triggered.connect(self.afficher_etat_options)  # 👈 ligne ajoutée
            options_menu.addAction(a)

        taille_menu = options_menu.addMenu("Taille police")
        self.taille_actions = []
        for taille in range(8, 25, 2):
            action = QAction(f"{taille} {'(défaut)' if taille==12 else ''}", self, checkable=True)
            action.setData(taille)
            action.triggered.connect(self.appliquer_taille_police)
            self.taille_actions.append(action)
            taille_menu.addAction(action)
        self.taille_actions[2].setChecked(True)

        #self.menu_bar.addMenu("Aide").addAction("À propos", self.ouvrir_fenetre_info)
        aide_menu = self.menu_bar.addMenu("?")

        # Action "Aide" avec explications
        action_aide = QAction("Aide", self)
        action_aide.triggered.connect(self.ouvrir_aide)  # méthode à créer
        aide_menu.addAction(action_aide)

        # Action "À propos" (inchangée)
        action_apropos = QAction("À propos", self)
        action_apropos.triggered.connect(self.ouvrir_fenetre_info)
        aide_menu.addAction(action_apropos)

        h_layout = QHBoxLayout()
        main_tab_layout.addLayout(h_layout)

        h_layout.addWidget(QLabel("Rechercher un motif :", font=QFont("Arial", 12)))

        self.entry = QLineEdit(placeholderText="Tapez un motif…")
        self.entry.setFont(QFont("Arial", 12))
        self.entry.textChanged.connect(self.filtrer_motifs)
        self.entry.setFixedWidth(400)
        h_layout.addWidget(self.entry)

        self.btn_clear = QPushButton("Effacer", font=QFont("Arial", 12, QFont.Bold))
        self.btn_clear.setMaximumWidth(120)
        self.btn_clear.clicked.connect(self.effacer_recherche)
        h_layout.addWidget(self.btn_clear)

        h_layout.addStretch()


        #self.lbl_result_count = QLabel("Nombre de résultats : 0", font=QFont("Arial", 11))
        #main_tab_layout.addWidget(self.lbl_result_count)

        self.tree = QTreeView()
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setUniformRowHeights(False)
        self.tree.setIconSize(QSize(30, 30))
        self.tree.setSelectionMode(QAbstractItemView.NoSelection)
        self.tree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tree.setItemDelegate(NoHoverDelegate())
        self.tree.setStyleSheet("""
            QTreeView::item { height: 36px; }
            QTreeView::item:hover { background-color: transparent; }
            QTreeView::item:selected { background-color: #3399FF; color: white; }
        """)
        self.tree.viewport().installEventFilter(self)
        main_tab_layout.addWidget(self.tree, stretch=1)
        self.entry.installEventFilter(self)

        self.model = QStandardItemModel(0, 6)
        headers = ["Image", "Item", "Motif", "Complement", "P", "Tri"]
        for i, h in enumerate(headers):
            self.model.setHeaderData(i, Qt.Horizontal, h)
        self.tree.setModel(self.model)
        self.tree.setItemDelegateForColumn(0, ImageCenterDelegate())

        header = self.tree.header()
        font_header = header.font()
        font_header.setBold(True)
        header.setFont(font_header)
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.resizeSection(0, 50)

        self.tooltip = ToolTip(self)
        self.appliquer_taille_police()

        # Onglet Bilans Simplifiés
        self.bilans_tab = BilansSimplifiesTab()
        self.tabs.addTab(self.bilans_tab, "Bilans simplifiés")
        
        self.bilans_tab.tree_bs.viewport().installEventFilter(self)
        self.bilans_tab.tree_bs.setItemDelegate(BilansTreeDelegate())

                # Onglet Plateau Caennais
        self.plateau_tab = PlateauCaennaisTab(self.plateau_data)
        self.tabs.addTab(self.plateau_tab, "Plateau Caennais")
        self.tabs.currentChanged.connect(self.onglet_change)

        
        for i in range(self.tabs.count()):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
            shortcut.activated.connect(lambda i=i: self.tabs.setCurrentIndex(i))

    def onglet_change(self, index):
        nom = self.tabs.tabText(index)
        self.status_left_label.setText(f"Onglet actif : {nom}")
        QTimer.singleShot(3000, lambda: self.status_left_label.setText("Prêt"))


    def afficher_etat_options(self):
        etats = []
        etats.append(f"Images {'✅' if self.afficher_images.isChecked() else '❌'}")
        etats.append(f"Couleurs {'✅' if self.afficher_couleurs.isChecked() else '❌'}")
        etats.append(f"Police {'✅' if self.afficher_mise_en_forme.isChecked() else '❌'}")
        etats.append(f"Taille {self.taille_police}")
        
        # Affichage dans la barre de statut à droite
        self.status_right_label.setText(" | ".join(etats))


        
        
    def appliquer_taille_police(self):
        sender = self.sender()
        if sender and sender.data():
            self.taille_police = sender.data()
        else:
            # Si aucun sender (au démarrage), utiliser taille 12 par défaut
            self.taille_police = 12

        # Mettre à jour le check des actions
        for action in self.taille_actions:
            action.setChecked(action.data() == self.taille_police)

        font = QFont("Helvetica", self.taille_police)
        self.tree.setFont(font)

        if hasattr(self, 'bilans_tab'):
            self.bilans_tab.set_font_size(self.taille_police)

        if hasattr(self, 'plateau_tab'):
            self.plateau_tab.set_font_size(self.taille_police)

        

        self.filtrer_motifs()

        self.status_bar.showMessage(f"Taille de police : {self.taille_police} pt", 3000)
        self.afficher_etat_options()

    def option_changee(self, action):
        self.filtrer_motifs()
        etat = "activée" if action.isChecked() else "désactivée"
        self.status_bar.showMessage(f"{action.text()} {etat}", 3000)

    
    def ajuster_largeur_colonnes(self):
        font = self.tree.font()
        header = self.tree.header()
        self.col_widths = [50]  # colonne image
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.resizeSection(0, 50)

        total_width = 50  # largeur initiale = colonne image

        for col in range(1, self.model.columnCount()):
            header_font = header.font()
            fm_header = QFontMetrics(header_font)
            max_width = fm_header.horizontalAdvance(str(self.model.headerData(col, Qt.Horizontal))) + 20

            for row in range(self.model.rowCount()):
                item = self.model.item(row, col)
                if not item:
                    continue
                text = item.text()
                font_item = item.font() if item.font() else font
                fm = QFontMetrics(font_item)
                largeur = fm.horizontalAdvance(text) + 20
                max_width = max(max_width, largeur)

            # Limiter les largeurs selon la colonne
            if col == 2:  # "Motif"
                max_width = min(max_width, 200)
            elif col == 3:  # "Complément"
                max_width = min(max_width, 400)
            else:
                max_width = min(max_width, 150)  # Limite raisonnable pour autres

            header.setSectionResizeMode(col, QHeaderView.Fixed)
            header.resizeSection(col, max_width)
            self.col_widths.append(max_width)
            total_width += max_width

        

        self.resize(total_width + 60, self.height())


    def ajuster_taille_fenetre(self, nb_lignes):
        row_height = self.tree.sizeHintForRow(0) or 32
        hauteur_tree = row_height * min(nb_lignes, 7)
        self.tree.setMinimumHeight(row_height * 7)
        self.tree.setMaximumHeight(16777215)

        largeur = 0
        for i in range(self.model.columnCount()):
            largeur += self.tree.columnWidth(i)
        largeur += 60

        autres_hauteurs = (
            self.menuBar().sizeHint().height() +
            self.entry.sizeHint().height() +
            self.btn_clear.sizeHint().height() +
            #self.lbl_result_count.sizeHint().height()
            + 40
        )
        self.resize(largeur, hauteur_tree + autres_hauteurs)
        self.tree.updateGeometry()


    def filtrer_motifs(self):
        texte = self.entry.text().strip().lower()
        
        self.model.removeRows(0, self.model.rowCount())

        if not texte:
            filtered_data = self.df
        else:
            filtered_data = [row for row in self.df if recherche(texte, [row["Motif"]])]


        if not filtered_data:
            #self.lbl_result_count.setText("<span style='color:red'><b>AUCUN MOTIF TROUVÉ</b></span>")
                # Créer une ligne vide avec le message dans la colonne "Motif" (index 2)
            empty_row = [QStandardItem("") for _ in range(self.model.columnCount())]
            
            message_item = QStandardItem("AUCUN MOTIF TROUVÉ")
            message_item.setForeground(QColor("red"))
            font = QFont("Arial", self.taille_police)
            font.setBold(True)
            message_item.setFont(font)
            message_item.setTextAlignment(Qt.AlignCenter)

            empty_row[2] = message_item  # Colonne "Motif"
            self.model.appendRow(empty_row)


            self.status_left_label.setText("Aucun motif trouvé.")
        else:
            #self.lbl_result_count.setText(f"{len(filtered_data)} motifs trouvés")
            self.status_left_label.setText(f"{len(filtered_data)} résultat(s) pour « {texte} »")


        for row in filtered_data:
            icon = QIcon()
            if self.afficher_images.isChecked():
                icon = charger_image(f'{row["Item"]}.png', self.base_dir) or QIcon()

            items = [
                QStandardItem(),
                QStandardItem(row["Item"]),
                QStandardItem(row["Motif"]),
                QStandardItem(row["Complement"]),
                QStandardItem(row["P"]),
                QStandardItem(row["Tri"])
            ]

            items[0].setData(icon, Qt.DecorationRole)
            items[0].setTextAlignment(Qt.AlignHCenter)

            # Appliquer la couleur de fond selon la priorité
            if self.afficher_couleurs.isChecked():
                if row["P"] == "P1":
                    couleur = QColor(255, 165, 0)  # orange
                elif row["P"] == "P2":
                    couleur = QColor(153, 204, 153)  # vert doux
                else:
                    couleur = None
                if couleur:
                    for it in items:
                        it.setBackground(couleur)

            # Appliquer la mise en forme police (gras/italique ou par défaut)
            if self.afficher_mise_en_forme.isChecked():
                tri = row["Tri"].lower()
                is_bold = tri == "mru"
                is_italic = tri == "mrl"

                for it in items:
                    custom_font = QFont(self.tree.font())  # Copie de la police actuelle
                    custom_font.setBold(is_bold)
                    custom_font.setItalic(is_italic)
                    it.setFont(custom_font)
            else:
                # Forcer la police même si pas de mise en forme
                font = QFont("Helvetica", self.taille_police)
                for it in items:
                    it.setFont(font)

            self.model.appendRow(items)

        self.ajuster_largeur_colonnes()
        self.ajuster_taille_fenetre(len(filtered_data))



    def effacer_recherche(self):
        self.entry.clear()


    

    def ouvrir_fenetre_info(self):
        dlg = HelpDialog(self)
        dlg.exec()

    def ouvrir_aide(self):
        texte = (
            "<h2>Guide d'utilisation du logiciel</h2>"
            "<p>Ce logiciel permet de rechercher des motifs, "
            "d’afficher les bilans simplifiés et de consulter le plateau Caennais.</p>"
            "<p><b>Comment l'utiliser :</b><br>"
            "- Tapez un motif dans le champ de recherche.<br>"
            "- Les recherches ne tiennent pas compte des accents ni des majuscules.<br>"
            "- La recherche s'effectue à chaque lettre saisie, il n'est pas nécessaire de taper le mot en entier.</p>"
            "<p><b>Raccourcis clavier :</b><br>"
            "Echap : Effacer recherche<br>"
            "Ctrl+1 : Recherche<br>"
            "Ctrl+2 : Bilan simplifié<br>"
            "Ctrl+3 : Plateau Caennais</p>"
            "<p>Options disponibles dans le menu Options pour personnaliser l’affichage.</p>"
        )
        QMessageBox.information(self, "Aide", texte)



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
