from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTreeView, QSizePolicy, QHeaderView
)
from PySide6.QtGui import QFont, QIcon, QStandardItem, QStandardItemModel, QColor, QFontMetrics
from PySide6.QtCore import Qt

from core.utils import supprimer_accents
from core.image_loader import charger_image
from core.delegates import NoHoverDelegate, ImageCenterDelegate


def init_main_tab(self):
    # Onglet principal
    main_tab = QWidget()
    self.tabs.addTab(main_tab, "Recherche")
    main_tab_layout = QVBoxLayout(main_tab)

    h_layout = QHBoxLayout()
    main_tab_layout.addLayout(h_layout)

    h_layout.addWidget(QLabel("Rechercher un motif :", font=QFont("Arial", 12)))

    self.entry = QLineEdit(placeholderText="Tapez un motif…")
    self.entry.setFont(QFont("Arial", 12))
    self.entry.textChanged.connect(self.filtrer_motifs)
    self.entry.setFixedWidth(400)
    h_layout.addWidget(self.entry)
    h_layout.addStretch()

    self.btn_clear = QPushButton("Effacer", font=QFont("Arial", 12, QFont.Bold))
    self.btn_clear.clicked.connect(self.effacer_recherche)
    main_tab_layout.addWidget(self.btn_clear)

    self.lbl_result_count = QLabel("Nombre de résultats : 0", font=QFont("Arial", 11))
    main_tab_layout.addWidget(self.lbl_result_count)

    self.tree = QTreeView()
    self.tree.setEditTriggers(QTreeView.NoEditTriggers)
    self.tree.setSelectionBehavior(QTreeView.SelectRows)
    self.tree.setAlternatingRowColors(True)
    self.tree.setRootIsDecorated(False)
    self.tree.setUniformRowHeights(False)
    self.tree.setIconSize(self.icon_size)
    self.tree.setSelectionMode(QTreeView.NoSelection)
    self.tree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.tree.setItemDelegate(NoHoverDelegate())
    self.tree.setStyleSheet("""
        QTreeView::item { height: 36px; }
        QTreeView::item:hover { background-color: transparent; }
        QTreeView::item:selected { background-color: #3399FF; color: white; }
    """)
    self.tree.viewport().installEventFilter(self)
    self.entry.installEventFilter(self)
    main_tab_layout.addWidget(self.tree, stretch=1)

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


def effacer_recherche(self):
    self.entry.clear()


def filtrer_motifs(self):
    texte = self.entry.text().strip().lower()
    recherche = supprimer_accents(texte)
    self.model.removeRows(0, self.model.rowCount())

    filtered_data = self.df if not texte else [row for row in self.df if recherche in supprimer_accents(row["Motif"].lower())]

    self.lbl_result_count.setText(
        f"<span style='color:red'><b>AUCUN MOTIF TROUVÉ</b></span>"
        if not filtered_data else f"{len(filtered_data)} motifs trouvés"
    )

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

        if self.afficher_couleurs.isChecked():
            if row["P"] == "P1":
                couleur = QColor(255, 165, 0)
            elif row["P"] == "P2":
                couleur = QColor(153, 204, 153)
            else:
                couleur = None
            if couleur:
                for it in items:
                    it.setBackground(couleur)

        if self.afficher_mise_en_forme.isChecked():
            tri = row["Tri"].lower()
            is_bold = tri == "mru"
            is_italic = tri == "mrl"
            for it in items:
                custom_font = QFont(self.tree.font())
                custom_font.setBold(is_bold)
                custom_font.setItalic(is_italic)
                it.setFont(custom_font)
        else:
            font = QFont("Helvetica", self.taille_police)
            for it in items:
                it.setFont(font)

        self.model.appendRow(items)

    self.ajuster_largeur_colonnes()
    self.ajuster_taille_fenetre(len(filtered_data))
