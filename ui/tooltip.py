# tooltip.py
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QPoint

class ToolTip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.ToolTip)
        self.label = QLabel(self)
        self.label.setStyleSheet("""
            background-color: #ffffe0;
            border: 1px solid black;
            padding: 2px;
            font-family: Arial;
            font-size: 10pt;
        """)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft)
        self.hide()

    def show_tooltip(self, text, x, y):
        
        self.label.setText(text)
        self.label.adjustSize()
        self.resize(self.label.size())
        self.move(QPoint(x, y))
        self.raise_()         # ✅ Ajoute cette ligne
        self.show() 
        #super().show()  # ✅ Appelle le vrai QWidget.show()

    def hide(self):
        super().hide()
