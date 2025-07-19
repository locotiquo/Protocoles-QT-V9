from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QFontMetrics
from PySide6.QtCore import Qt


class BilansSimplifiesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.font_size = 12
        self.layout = QVBoxLayout(self)
        self.header_labels = ["Constantes", "Situation Clinique", "Non BS", "Contexte"]
        self.build_table()

    def build_table(self):
        self.tree_bs = QTreeView()
        self.model = QStandardItemModel(0, len(self.header_labels))
        self.model.setHorizontalHeaderLabels(self.header_labels)
        self.model_bs = self.model
        self.tree_bs.setModel(self.model)

        self.tree_bs.setAlternatingRowColors(True)
        self.tree_bs.setRootIsDecorated(False)
        self.tree_bs.setEditTriggers(QTreeView.NoEditTriggers)
        self.tree_bs.setSelectionMode(QTreeView.NoSelection)
        self.tree_bs.setStyleSheet("""
            QHeaderView::section {
                background-color: #FFA500;
                color: black;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #d9d9d9;
            }
        """)

        header = self.tree_bs.header()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.layout.addWidget(self.tree_bs)

        self.populate_data()

    def populate_data(self):
        data = [
            ("Pouls (<50 ou >110)", "Trouble de la conscience", "Absence de regulation", "<18 ans"),
            ("TA (<9 ou >180)", "AVC", "Absence d'observation", "AVP"),
            ("Sat (<94 ou <89 BPCO)", "Dlr tho persistante", "Pas de nom de MR", "Trauma avec déformation"),
            ("FR (<12 ou >25)", "Hyperalgie", "PRPA", "Chute >3m"),
            ("T (<35 ou >38,5)", "Saignement actif malgré compression", "Relevage non régulé", "Bilan SMUR"),
            ("", "TOUT NOUVEAU SYMPTOME", "Laissé sur place", "")
        ]

        for row in data:
            items = [QStandardItem(cell) for cell in row]
            for item in items:
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Arial", self.font_size))
            self.model.appendRow(items)

        self.ajuster_largeur_colonnes()

    def set_font_size(self, size):
        self.font_size = size
        font = QFont("Arial", size)

        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                item = self.model.item(row, col)
                if item:
                    item.setFont(font)

        header = self.tree_bs.header()
        header.setFont(font)
        header.setMinimumHeight(QFontMetrics(font).height() + 12)
        header.resizeSections(QHeaderView.ResizeToContents)

        self.ajuster_largeur_colonnes()

    def ajuster_largeur_colonnes(self):
        self.tree_bs.header().setSectionResizeMode(QHeaderView.ResizeToContents)
