from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QTreeView, QHeaderView, QAbstractItemView, QSizePolicy, QTabWidget
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QColor
from PySide6.QtCore import Qt, QSize, QTimer, QEvent, QPoint

from ui.tooltip import ToolTip
from ui.bilans_tab import BilansSimplifiesTab
from ui.plateau_tab import PlateauCaennaisTab
from ui.fiches_pratiques_tab import FichesPratiquesTab
from ui.delegates import NoHoverDelegate, BilansTreeDelegate, ImageCenterDelegate
from ui.menus import creer_menus

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

    # Création de la barre de menu (inclut taille_actions et options)
    self.menu_bar = creer_menus(self)
    self.setMenuBar(self.menu_bar)

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

    # Onglet Fiches pratiques
    self.fiches_tab = FichesPratiquesTab(self.base_dir)
    self.tabs.addTab(self.fiches_tab, "Fiches pratiques")
