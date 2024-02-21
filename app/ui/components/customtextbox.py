from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPainter, QPalette


class CustomTextBox(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            '''
            QLineEdit {
                background-color: transparent;
                border:2px solid;
                border-radius: 5px;
                border-color: #ffffff;
                font-size: 18px; 
                color: #ffffff; 
                font-weight: bold;
                height: 40px;
                width: 10px;
            }
            '''
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        border_color = self.palette().color(QPalette.Text)
        border_color.setAlpha(50)
        painter.setPen(border_color)

        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            5,
            5
        )

        super().paintEvent(event)


class CustomTextBoxForImageGen(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            '''
            QLineEdit {
                background-color: transparent;
                border:1.2px solid;
                border-radius: 5px;
                border-color: #fae69e;
                font-size: 18px; 
                color: #ffffff; 
                padding: 8px 16px;
                font-weight: semi-bold;
                height: 40px;
            }
            '''
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        border_color = self.palette().color(QPalette.Text)
        border_color.setAlpha(50)
        painter.setPen(border_color)

        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            5,
            5
        )

        super().paintEvent(event)