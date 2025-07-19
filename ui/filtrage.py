from PySide6.QtGui import QStandardItem, QFont, QColor, QIcon
from PySide6.QtCore import Qt
from core.image_loader import charger_image
from core.utils import recherche

def filtrer_motifs(self):
    texte = self.entry.text().strip().lower()
    self.model.removeRows(0, self.model.rowCount())

    if not texte:
        filtered_data = self.df
    else:
        filtered_data = [row for row in self.df if recherche(texte, [row["Motif"]])]

    if not filtered_data:
        empty_row = [QStandardItem("") for _ in range(self.model.columnCount())]
        message_item = QStandardItem("AUCUN MOTIF TROUVÉ")
        message_item.setForeground(QColor("red"))
        font = QFont("Arial", self.taille_police)
        font.setBold(True)
        message_item.setFont(font)
        message_item.setTextAlignment(Qt.AlignCenter)
        empty_row[2] = message_item
        self.model.appendRow(empty_row)
        self.status_left_label.setText("Aucun motif trouvé.")
        return

    self.status_left_label.setText(f"{len(filtered_data)} résultat(s) pour « {texte} »")

    for row in filtered_data:
        icon = QIcon()
        if self.afficher_images.isChecked():
            icon = charger_image(f'{row["Item"]}.png', self.base_dir) or QIcon()

        items = [
            QStandardItem(),  # Image
            QStandardItem(row["Item"]),
            QStandardItem(row["Motif"]),
            QStandardItem(row["Complement"]),
            QStandardItem(row["P"]),
            QStandardItem(row["Tri"])
        ]
        items[0].setData(icon, Qt.DecorationRole)
        items[0].setTextAlignment(Qt.AlignHCenter)

        if self.afficher_couleurs.isChecked():
            couleur = None
            if row["P"] == "P1":
                couleur = QColor(255, 165, 0)
            elif row["P"] == "P2":
                couleur = QColor(153, 204, 153)
            if couleur:
                for it in items:
                    it.setBackground(couleur)

        if self.afficher_mise_en_forme.isChecked():
            tri = row["Tri"].lower()
            is_bold = tri == "mru"
            is_italic = tri == "mrl"
            for it in items:
                font = QFont(self.tree.font())
                font.setBold(is_bold)
                font.setItalic(is_italic)
                it.setFont(font)
        else:
            font = QFont("Helvetica", self.taille_police)
            for it in items:
                it.setFont(font)

        self.model.appendRow(items)

    self.ajuster_largeur_colonnes()
    self.ajuster_taille_fenetre(len(filtered_data))
