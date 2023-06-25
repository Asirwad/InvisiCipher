from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPaintEvent
from PyQt5.QtWidgets import QWidget


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = None

    def set_background_image(self, image_path):
        self.background_image = QPixmap(image_path)
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        if self.background_image:
            pixmap = self.background_image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            x_offset = (pixmap.width() - self.width()) // 2
            y_offset = (pixmap.height() - self.height()) // 2
            painter.drawPixmap(-x_offset, -y_offset, pixmap)
