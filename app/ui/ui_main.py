from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QListWidget, QStackedWidget, QWidget
from app.ui.windows.hideImagePage import HideImagePage
from app.ui.windows.retrieveImagePage import RetrieveImagePage
from app.ui.windows.superResPage import SuperResolutionPage


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create UI elements for the main menu
        self.list_widget = QListWidget
        self.stacked_widget = QStackedWidget

        # Add functionality pages to the stacked widget
        self.stacked_widget.addWidget(HideImagePage())
        self.stacked_widget.addWidget(RetrieveImagePage())
        self.stacked_widget.addWidget((SuperResolutionPage()))

        # Connect the list widget to the stacked widget
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Create layout for the main menu
        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.stacked_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication([])
    main_menu = MainMenu()
    main_menu.show()
    app.exec_()
