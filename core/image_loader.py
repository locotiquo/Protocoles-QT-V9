import os
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt

def charger_image(image_name, base_dir):
    image_path = os.path.join(base_dir, "resources", "image", image_name)
    if not os.path.exists(image_path):
        return None
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        return None
    pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return QIcon(pixmap)
