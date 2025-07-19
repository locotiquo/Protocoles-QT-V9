from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView,
    QLineEdit, QPushButton
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt, QEvent
from core.utils import supprimer_accents


class PlateauCaennaisTab(QWidget):
    def __init__(self, plateau_data):
        super().__init__()
        self.plateau_data = plateau_data

        self.hopitaux = ["CHU", "HPSM", "Le Parc", "Misericorde"]
        self.table_font_size = 12  # police par défaut

        main_layout = QVBoxLayout(self)

        # ===== Champ recherche + bouton effacer =====
        search_layout = QHBoxLayout()
        label_search = QLabel("Rechercher :")
        font_bold = QFont()
        font_bold.setBold(True)
        label_search.setFont(font_bold)
        search_layout.addWidget(label_search)

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Tapez un texte…")
        self.search_entry.setFont(font_bold)
        self.search_entry.textChanged.connect(self.filtrer_motifs)
        self.search_entry.installEventFilter(self)
        search_layout.addWidget(self.search_entry)

        self.btn_clear = QPushButton("Effacer")
        self.btn_clear.setFont(font_bold)
        self.btn_clear.clicked.connect(self.effacer_tout)
        search_layout.addWidget(self.btn_clear)

        main_layout.addLayout(search_layout)

        # ===== Combo Thème (vide par défaut) =====
        theme_layout = QHBoxLayout()
        label_theme = QLabel("Thème :")
        label_theme.setFont(font_bold)
        theme_layout.addWidget(label_theme)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem("— Thème —")  # valeur vide par défaut
        self.theme_combo.setFont(font_bold)
        self.theme_combo.currentTextChanged.connect(self.filtrer_motifs)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()

        main_layout.addLayout(theme_layout)

        # ===== Table des motifs (2 colonnes) =====
        self.motif_table = QTableWidget()
        self.motif_table.setColumnCount(2)
        self.motif_table.setHorizontalHeaderLabels(["", ""])
        self.motif_table.verticalHeader().setVisible(False)
        self.motif_table.horizontalHeader().setVisible(False)
        self.motif_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.motif_table.setSelectionBehavior(QTableWidget.SelectItems)
        self.motif_table.setSelectionMode(QTableWidget.SingleSelection)
        self.motif_table.cellClicked.connect(self.on_motif_selected)
        self.motif_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        header = self.motif_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        main_layout.addWidget(self.motif_table)

        # ===== Résultats : label + tableau centré =====
        main_layout.addSpacing(12)
        label_pris_charge = QLabel("Peut prendre en charge :")
        font_bold.setPointSize(14)
        label_pris_charge.setFont(font_bold)
        main_layout.addWidget(label_pris_charge, alignment=Qt.AlignHCenter)

        self.table = QTableWidget(1, len(self.hopitaux))
        self.table.setHorizontalHeaderLabels(self.hopitaux)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.table.setMinimumHeight(80)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.motif_table.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #CCE5FF;  /* bleu clair surbrillance */
                color: black;
                border: 1px solid black;
            }
        """)

        main_layout.addWidget(self.table, alignment=Qt.AlignHCenter)
        main_layout.addSpacing(5)

        # Initialisations
        self.filtered_data = self.plateau_data  # données filtrées en cours

        self.set_font_size(self.table_font_size)
        self.filtrer_motifs()  # lance un filtrage au départ

    def filtrer_motifs(self):
        texte = supprimer_accents(self.search_entry.text().strip().lower())
        selected_theme = self.theme_combo.currentText()
        theme_filtre = selected_theme if selected_theme != "— Thème —" else None

        # Filtrer selon texte sur motif ou thème
        if texte:
            self.filtered_data = [
                row for row in self.plateau_data
                if texte in supprimer_accents(row["Motif"].lower()) or texte in supprimer_accents(row["Theme"].lower())
            ]
        else:
            self.filtered_data = self.plateau_data

        # Met à jour la liste des thèmes en fonction des résultats filtrés
        themes_disponibles = sorted(set(row["Theme"] for row in self.filtered_data), key=str.lower)

        # Mise à jour combo thèmes sans déclencher signal
        self.theme_combo.blockSignals(True)
        current_theme = self.theme_combo.currentText()
        self.theme_combo.clear()
        self.theme_combo.addItem("— Thème —")
        self.theme_combo.addItems(themes_disponibles)

        if current_theme in themes_disponibles:
            index = self.theme_combo.findText(current_theme)
            self.theme_combo.setCurrentIndex(index)
            theme_filtre = current_theme
        else:
            self.theme_combo.setCurrentIndex(0)
            theme_filtre = None

        self.theme_combo.blockSignals(False)

        # Appliquer filtre thème si défini
        if theme_filtre:
            self.filtered_data = [row for row in self.filtered_data if row["Theme"] == theme_filtre]

        # Afficher les motifs ou vider la table si rien
        if self.filtered_data:
            self.afficher_motifs()
        else:
            self.motif_table.setRowCount(0)
            for col in range(len(self.hopitaux)):
                self.table.setItem(0, col, QTableWidgetItem(""))

    def afficher_motifs(self):
        motifs = [row["Motif"] for row in self.filtered_data]
        row_count = (len(motifs) + 1) // 2
        self.motif_table.setRowCount(row_count)

        for i in range(row_count):
            for j in range(2):
                index = i * 2 + j
                if index < len(motifs):
                    text = motifs[index]
                    item = QTableWidgetItem(text)
                    item.setTextAlignment(Qt.AlignCenter)
                    font = QFont()
                    font.setPointSize(self.table_font_size)
                    item.setFont(font)
                    self.motif_table.setItem(i, j, item)
                else:
                    self.motif_table.setItem(i, j, QTableWidgetItem(""))

        self.motif_table.resizeRowsToContents()

        if motifs:
            self.motif_table.setCurrentCell(0, 0)
            self.on_motif_changed(motifs[0])
        else:
            for col in range(len(self.hopitaux)):
                self.table.setItem(0, col, QTableWidgetItem(""))

    def on_motif_selected(self, row, col):
        item = self.motif_table.item(row, col)
        if item and item.text():
            self.on_motif_changed(item.text())

    def on_motif_changed(self, motif):
        selected_theme = self.theme_combo.currentText()
        if selected_theme == "— Thème —":
            # Pas de thème filtré, on cherche dans tous les résultats filtrés
            match = next((r for r in self.filtered_data if r["Motif"] == motif), None)
        else:
            # Recherche dans le thème filtré uniquement
            match = next((r for r in self.filtered_data if r["Theme"] == selected_theme and r["Motif"] == motif), None)
        if not match:
            return

        for col, hopital in enumerate(self.hopitaux):
            cell = QTableWidgetItem()
            if match[hopital].strip():
                cell.setText("✔️")
                cell.setTextAlignment(Qt.AlignCenter)
                cell.setBackground(QColor("#7BA05B"))
            else:
                cell.setText("✖️")
                cell.setTextAlignment(Qt.AlignCenter)
                cell.setBackground(QColor("#e12929"))

            font = QFont()
            font.setPointSize(self.table_font_size)
            font.setBold(True)
            cell.setFont(font)
            self.table.setItem(0, col, cell)

        self.table.resizeColumnsToContents()

    def effacer_tout(self):
        self.search_entry.clear()
        self.theme_combo.setCurrentIndex(0)  # remet "— Thème —"
        self.filtered_data = self.plateau_data
        self.filtrer_motifs()

    def set_font_size(self, taille):
        self.table_font_size = taille
        font = QFont()
        font.setPointSize(taille)

        self.search_entry.setFont(font)
        self.theme_combo.setFont(font)
        self.motif_table.setFont(font)
        self.table.setFont(font)

        # Met à jour la police de chaque item dans motif_table
        for row in range(self.motif_table.rowCount()):
            for col in range(self.motif_table.columnCount()):
                item = self.motif_table.item(row, col)
                if item is not None:
                    item_font = item.font()
                    item_font.setPointSize(taille)
                    item.setFont(item_font)

        self.table.setRowHeight(0, taille + 30)
        self.table.setFixedHeight(taille + 60)

        self.motif_table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

        # Ajuste la largeur minimale du tableau résultats si besoin
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        self.table.setMinimumWidth(total_width + 10)

    def eventFilter(self, source, event):
        # Ajout gestion touche Échap dans champ recherche pour effacer
        if source == self.search_entry and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.effacer_tout()
                return True
        return super().eventFilter(source, event)
