import sys

from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QDialog, QVBoxLayout, QRadioButton, \
    QStyleFactory, QAbstractItemView, QHeaderView, QTreeView, QStyledItemDelegate


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'InvisiCipher'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create a navigation bar
        nav_bar = NavigationBar(self)
        nav_bar_model = QStandardItemModel()
        nav_bar.setModel(nav_bar_model)
        nav_bar.setUniformRowHeights(True)
        nav_bar.setWordWrap(True)
        nav_bar.setColumnWidth(0, 200)
        nav_bar.clicked.connect(self.on_nav_bar_clicked)

        # Add items to the navigation bar
        hide_image_item = QStandardItem(QIcon('icons/image.svg'), 'Hide Image')
        hide_image_item.setToolTip('Hide the currently displayed image')
        nav_bar_model.appendRow(hide_image_item)

        reveal_image_item = QStandardItem(QIcon('icons/search.svg'), 'Reveal Image')
        reveal_image_item.setToolTip('Reveal the currently hidden image')
        nav_bar_model.appendRow(reveal_image_item)

        upscale_image_item = QStandardItem(QIcon('icons/shield.svg'), 'Upscale Image')
        upscale_image_item.setToolTip('Upscale the currently displayed image')
        nav_bar_model.appendRow(upscale_image_item)

        settings_item = QStandardItem(QIcon('icons/settings.svg'), 'Settings')
        settings_item.setToolTip('Open the settings dialog')
        nav_bar_model.appendRow(settings_item)

        self.setCentralWidget(nav_bar)
        self.show()

    def on_nav_bar_clicked(self, index):
        item = index.model().itemFromIndex(index)
        function_name = item.text()
        function_description = item.toolTip()
        print(function_name, function_description)

    def show_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec_()


class NavigationBar(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setIndentation(0)
        self.setAnimated(True)
        self.setExpandsOnDoubleClick(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setUniformRowHeights(True)
        self.setWordWrap(True)
        self.setSortingEnabled(True)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)

        delegate = QStyledItemDelegate(self)
        self.setItemDelegate(delegate)

        self.setStyleSheet(open('Styles/dark.css').read())

    def setModel(self, model):
        super().setModel(model)
        self.expandAll()


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.layout = QVBoxLayout()
        self.dark_mode_radio = QRadioButton('Dark Mode')
        self.light_mode_radio = QRadioButton('Light Mode')
        self.dark_mode_radio.setChecked(True)
        self.dark_mode_radio.toggled.connect(self.set_dark_mode)
        self.light_mode_radio.toggled.connect(self.set_light_mode)
        self.layout.addWidget(self.dark_mode_radio)
        self.layout.addWidget(self.light_mode_radio)
        self.setLayout(self.layout)

    def set_dark_mode(self, checked):
        if checked:
            self.parent().setStyleSheet('background-color: #1E1E1E; color: #FFFFFF;')
            self.parent().setPalette(QApplication.palette())
            QApplication.setStyle(QStyleFactory.create('Fusion'))

    def set_light_mode(self, checked):
        if checked:
            self.parent().setStyleSheet('')
            self.parent().setPalette(QApplication.palette())
            QApplication.setStyle(QStyleFactory.create('Fusion'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
