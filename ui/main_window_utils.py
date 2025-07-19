from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView


def ajuster_largeur_colonnes(self):
    font = self.tree.font()
    header = self.tree.header()
    self.col_widths = [50]  # colonne image
    header.setSectionResizeMode(0, QHeaderView.Fixed)
    header.resizeSection(0, 50)

    total_width = 50

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

        if col == 2:
            max_width = min(max_width, 200)
        elif col == 3:
            max_width = min(max_width, 400)
        else:
            max_width = min(max_width, 150)

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
        40
    )
    self.resize(largeur, hauteur_tree + autres_hauteurs)
    self.tree.updateGeometry()
