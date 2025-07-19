# ui/setup_ui.py
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTreeView, QMenuBar,
    QSizePolicy, QTabWidget, QHeaderView
)
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtCore import QSize

from ui.bilans_tab import BilansSimplifiesTab
from ui.plateau_tab import PlateauCaennaisTab
from ui.tooltip import ToolTip
from ui.delegates import NoHoverDelegate, ImageCenterDelegate, BilansTreeDelegate
from core.image_loader import charger_image
from core.utils import get_icon_path


def setup_ui(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    main_layout = QVBoxLayout(central_widget)

    self.tabs = QTabWidget()
    main_layout.addWidget(self.tabs)

    # Onglet principal
    main_tab = QWidget()
    self.tabs.addTab(main_tab, "Recherche")
    main_tab_layout = QVBoxLayout(main_tab)

    # Menu principal
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
        a.triggered.connect(self.afficher_etat_options)
        options_menu.addAction(a)

    taille_menu = options_menu.addMenu("Taille police")
    self.taille_actions = []
    for taille in range(8, 25, 2):
        action = QAction(f"{taille} {'(défaut)' if taille == 12 else ''}", self, checkable=True)
        action.setData(taille)
        action.triggered.connect(self.appliquer_taille_police)
        self.taille_actions.append(action)
        taille_menu.addAction(action)
    self.taille_actions[2].setChecked(True)

    self.menu_bar.addMenu("Aide").addAction("À propos", self.ouvrir_fenetre_info)

    # Ligne de recherche
    h_layout = QHBoxLayout()
    main_tab_layout.addLayout(h_layout)
    h_layout.addWidget(QLabel("Rechercher un motif :", font=QFont("Arial", 12)))
    self.entry = QLineEdit(placeholderText="Tapez un motif…")
    self.entry.setFont(QFont("Arial", 12))
    self.entry.textChanged.connect(self.filtrer_motifs)
    self.entry.setFixedWidth(400)
    h_layout.addWidget(self.entry)

    self.btn_clear = QPushButton("Effacer", font=QFont("Arial", 12))
    self.btn_clear.setMaximumWidth(120)
    self.btn_clear.clicked.connect(self.effacer_recherche)
    h_layout.addWidget(self.btn_clear)

    h_layout.addStretch()

    self.tree = QTreeView()
    self.tree.setEditTriggers(QTreeView.NoEditTriggers)
    self.tree.setSelectionBehavior(QTreeView.SelectRows)
    self.tree.setAlternatingRowColors(True)
    self.tree.setRootIsDecorated(False)
    self.tree.setUniformRowHeights(False)
    self.tree.setIconSize(QSize(30, 30))
    self.tree.setSelectionMode(QTreeView.NoSelection)
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

    self.tooltip = ToolTip(self)

    # Onglet Bilans Simplifiés
    self.bilans_tab = BilansSimplifiesTab()
    self.tabs.addTab(self.bilans_tab, "Bilans simplifiés")
    self.bilans_tab.tree_bs.viewport().installEventFilter(self)
    self.bilans_tab.tree_bs.setItemDelegate(BilansTreeDelegate())

    # Onglet Plateau Caennais
    self.plateau_tab = PlateauCaennaisTab(self.plateau_data)
    self.tabs.addTab(self.plateau_tab, "Plateau Caennais")
    self.tabs.currentChanged.connect(self.onglet_change)

    # Icone
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        self.setWindowIcon(QIcon(icon_path))
