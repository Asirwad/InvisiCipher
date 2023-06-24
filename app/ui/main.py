import os
import sys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QLabel, QMessageBox, QProgressBar, QFileDialog, QSizePolicy, QLayout, QDialog
from PyQt5.QtCore import Qt
from app.models.ESRGAN import RRDBNet_arch as arch
import torch
import cv2
import numpy as np


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.low_res_image_text_label = None
        self.image_label = None
        self.low_res_image_filepath = None
        self.download_button = None
        self.setWindowTitle("InvisiCipher")
        self.setGeometry(200, 200, 1400, 800)
        self.setWindowIcon(QIcon("icon.ico"))
        self.setStyleSheet("background-color: #2b2b2b;")
        self.setFixedSize(self.size())

        # Set up the main window layout
        main_layout = QHBoxLayout()

        # Create the side navigation bar
        side_navigation = QWidget()
        side_navigation.setObjectName("side_navigation")
        side_navigation.setFixedWidth(200)
        side_layout = QVBoxLayout()

        # Create buttons for each option
        encryption_button = QPushButton("Encryption")
        decryption_button = QPushButton("Decryption")
        image_hiding_button = QPushButton("Image Hiding")
        image_reveal_button = QPushButton("Image Reveal")
        super_resolution_button = QPushButton("Super Resolution")

        # Connect button signals to their corresponding slots
        encryption_button.clicked.connect(self.show_encryption_page)
        decryption_button.clicked.connect(self.show_decryption_page)
        image_hiding_button.clicked.connect(self.show_image_hiding_page)
        image_reveal_button.clicked.connect(self.show_reveal_page)
        super_resolution_button.clicked.connect(self.show_super_resolution_page)

        # Add buttons to the side navigation layout
        side_layout.addWidget(encryption_button)
        side_layout.addWidget(decryption_button)
        side_layout.addWidget(image_hiding_button)
        side_layout.addWidget(image_reveal_button)
        side_layout.addWidget(super_resolution_button)

        # Add a logout button
        logout_button = QPushButton("Logout")
        logout_button.setObjectName("logout_button")
        logout_button.clicked.connect(self.logout)
        side_layout.addStretch()
        side_layout.addWidget(logout_button)

        # Set the layout for the side navigation widget
        side_navigation.setLayout(side_layout)

        # Create the main content area
        main_content = QWidget()
        main_content.setObjectName("main_content")
        self.main_layout = QVBoxLayout()
        main_content.setLayout(self.main_layout)

        # Add the side navigation and main content to the main window layout
        main_layout.addWidget(side_navigation)
        main_layout.addWidget(main_content)

        # Set the main window layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_encryption_page(self):
        # Clear the main layout
        self.clear_main_layout()

        # Create widgets for the encryption page
        title_label = QLabel("Encryption Page")
        input_label = QLabel("Enter the text to encrypt:")
        input_text = QLineEdit()
        encrypt_button = QPushButton("Encrypt")

        # Create a layout for the encryption page
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(input_label)
        layout.addWidget(input_text)
        layout.addWidget(encrypt_button)

        # Create a widget for the encryption page and set the layout
        page_widget = QWidget()
        page_widget.setLayout(layout)

        # Add the encryption page widget to the main layout
        self.main_layout.addWidget(page_widget)

    def show_decryption_page(self):
        self.clear_main_layout()

        title_label = QLabel("Decryption Page")
        input_label = QLabel("Enter the text to decrypt:")
        input_text = QLineEdit()
        decrypt_button = QPushButton("Decrypt")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(input_label)
        layout.addWidget(input_text)
        layout.addWidget(decrypt_button)

        page_widget = QWidget()
        page_widget.setLayout(layout)

        self.main_layout.addWidget(page_widget)

    def show_image_hiding_page(self):
        self.clear_main_layout()

        title_label = QLabel("Hide Page")
        input_label = QLabel("Select the cover image:")
        cover_image_button = QPushButton("Browse")
        input_label_2 = QLabel("Select the secret image:")
        secret_image_button = QPushButton("Browse")
        hide_button = QPushButton("Hide")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(input_label)
        layout.addWidget(cover_image_button)
        layout.addWidget(input_label_2)
        layout.addWidget(secret_image_button)
        layout.addWidget(hide_button)

        page_widget = QWidget()
        page_widget.setLayout(layout)

        self.main_layout.addWidget(page_widget)

    def show_reveal_page(self):
        self.clear_main_layout()

        title_label = QLabel("Reveal Page")
        input_label = QLabel("Select the steg image:")
        steg_image_button = QPushButton("Browse")
        reveal_button = QPushButton("Reveal")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(input_label)
        layout.addWidget(steg_image_button)
        layout.addWidget(reveal_button)

        page_widget = QWidget()
        page_widget.setLayout(layout)

        self.main_layout.addWidget(page_widget)

    def show_super_resolution_page(self):
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>Enhanced Super Resolution using ESRGAN</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff; margin-bottom: 20px;")
        self.main_layout.addWidget(title_label)

        # ESRGAN model path label
        model_path_label = QLabel("<h5>Model Path: InvisiCipher/app/models/ESRGAN/models/RRDB_ESRGAN_x4.pth</h5>")
        model_path_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 20px;")
        self.main_layout.addWidget(model_path_label)

        # Low resolution image selection
        low_res_label = QLabel("Select Low Resolution Image:")
        low_res_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        self.main_layout.addWidget(low_res_label)

        # image display
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(image_label)

        # Create a progress bar widget
        progress_bar = QProgressBar(self)
        progress_bar.setGeometry(10, 220, 200, 20)

        # defining button layout
        button_layout = QHBoxLayout()

        # Browse button
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.select_low_resolution_image(image_label))
        button_layout.addWidget(browse_button)

        # Up-scale button
        upscale_button = QPushButton("UP-SCALE")
        upscale_button.clicked.connect(lambda: self.upscaleImage(image_label))
        button_layout.addWidget(upscale_button)

        # Download button
        download_button = QPushButton("Download")
        download_button.setEnabled(False)
        download_button.clicked.connect(self.download_high_resolution_image)
        button_layout.addWidget(download_button)

        # add the button layout to the main layout
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_widget)

        # Set the image labels as attributes
        self.low_res_image_text_label = low_res_label
        self.image_label = image_label
        self.download_button = download_button

    def select_low_resolution_image(self, label):
        file_dialog = QFileDialog()
        low_res_image_filepath, _ = file_dialog.getOpenFileName(self, "Select Low Resolution Image")
        if low_res_image_filepath:
            self.low_res_image_filepath = low_res_image_filepath
            pixmap = QPixmap(low_res_image_filepath)
            label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def upscaleImage(self, label):
        if self.low_res_image_filepath is None:
            QMessageBox.information(self, "Upscaling Error", "Please select the low-resolution image first.")
            return
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:400"
        model_path = 'C:/Users/asirw/PycharmProjects/InvisiCipher/app/models/ESRGAN/models/RRDB_ESRGAN_x4.pth'
        device = torch.device('cuda')

        model = arch.RRDBNet(3, 3, 64, 23, gc=32)
        model.load_state_dict(torch.load(model_path), strict=True)
        model.eval()
        model = model.to(device)

        print('Model path {:s}. \nUp-scaling...'.format(model_path))

        image = cv2.imread(self.low_res_image_filepath, cv2.IMREAD_COLOR)
        image = image * 1.0 / 255
        image = torch.from_numpy(np.transpose(image[:, :, [2, 1, 0]], (2, 0, 1))).float()
        image_low_res = image.unsqueeze(0)
        image_low_res = image_low_res.to(device)

        with torch.no_grad():
            image_high_res = model(image_low_res).data.squeeze().float().cpu().clamp_(0, 1).numpy()
        image_high_res = np.transpose(image_high_res[[2, 1, 0], :, :], (1, 2, 0))
        image_high_res = (image_high_res * 255.0).round()

        high_res_image_path = os.path.abspath('upscaled.png')
        cv2.imwrite(high_res_image_path, image_high_res)

        # Display the high resolution image
        if os.path.exists(high_res_image_path):
            print("image saved as: ", high_res_image_path)
            pixmap = QPixmap(high_res_image_path).scaled(400, 400, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            self.low_res_image_text_label.setText("High Res Image:")
            self.download_button.setEnabled(True)
        else:
            QMessageBox.critical(self, "Upscaling Error", "Failed to upscale the image.")

    def download_high_resolution_image(self):
        # Implement the logic to download the high resolution image
        QMessageBox.information(self, "Download", "Downloading the high resolution image...")

    def clear_main_layout(self):
        # Remove all widgets from the main layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def logout(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Logout")
        dialog.setMinimumSize(200, 100)

        layout = QVBoxLayout(dialog)
        msg_box = QMessageBox()
        msg_box.setText("Are you sure you want to logout?")

        # Set custom font and size
        font = QFont("Arial", 12)  # Adjust the font and size as desired
        msg_box.setFont(font)

        button_layout = QHBoxLayout()
        layout.addWidget(msg_box)
        layout.addLayout(button_layout)

        # Remove the standard buttons
        msg_box.setStandardButtons(QMessageBox.NoButton)

        yes_button = QPushButton("Yes")
        yes_button.setStyleSheet("color: #000000;")
        yes_button.clicked.connect(lambda: QApplication.quit())

        no_button = QPushButton("No")
        no_button.setStyleSheet("color: #000000;")
        no_button.clicked.connect(dialog.reject)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        dialog.exec_()

    def load_stylesheet(self):
        stylesheet = QFile("styles/style.css")
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            self.setStyleSheet(stream.readAll())


# Create the application
app = QApplication(sys.argv)
window = MainAppWindow()
window.load_stylesheet()
window.show()
sys.exit(app.exec_())
