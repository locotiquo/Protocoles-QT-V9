from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

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
