import os
import sys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QLabel, QMessageBox, QProgressBar, QFileDialog, QSizePolicy, QLayout, QDialog, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt
from app.ui.components.backgroundwidget import BackgroundWidget
from app.ui.components.customtextbox import CustomTextBox
from app.models.encryption import aes, blowfish
from app.models.DEEP_STEGO.hide_image import hide_image
from app.models.DEEP_STEGO.reveal_image import reveal_image
from app.models.ESRGAN import RRDBNet_arch as arch
import torch
import cv2
import numpy as np


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # vars
        self.main_content = None
        self.blowfish_radio_dec = None
        self.aes_radio_dec = None
        self.key_text_box_of_dec = None
        self.enc_filepath = None
        self.dec_display_label = None
        self.download_dec_button = None
        self.dec_img_text_label = None
        self.enc_img_text_label = None
        self.key_text_box = None
        self.blowfish_radio = None
        self.aes_radio = None
        self.image_tobe_enc_filepath = None
        self.download_enc_button = None
        self.enc_display_label = None
        self.container_image_filepath = None
        self.secret_out_display_label = None
        self.container_display_label = None
        self.download_revealed_secret_image_button = None
        self.download_steg_button = None
        self.secret_image_filepath = None
        self.cover_image_filepath = None
        self.steg_display_label = None
        self.secret_display_label = None
        self.cover_display_label = None
        self.low_res_image_text_label = None
        self.image_label = None
        self.low_res_image_filepath = None
        self.download_HR_button = None

        # Set window properties
        self.setWindowTitle("InvisiCipher")
        self.setGeometry(200, 200, 1400, 800)
        self.setWindowIcon(QIcon("icon.ico"))
        self.setStyleSheet("background-color: #2b2b2b;")
        self.setFixedSize(self.size())
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Set up the main window layout
        main_layout = QHBoxLayout()

        # Create the side navigation bar
        side_navigation = BackgroundWidget()
        side_navigation.set_background_image("assets/components_backgrounds/sidebar_bg.jpg")
        side_navigation.setObjectName("side_navigation")
        side_navigation.setFixedWidth(200)
        side_layout = QVBoxLayout()

        # label for logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png").scaled(50, 50, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # label for logo name
        name_label = QLabel()
        name_label.setText("<h2>InvisiCipher</h2><br><br><br><br><br><br><br><br><br>")
        name_label.setStyleSheet("color: #ffffff;")
        name_label.setAlignment(Qt.AlignCenter)

        # Create buttons for each option
        encryption_button = QPushButton("Encryption")
        decryption_button = QPushButton("Decryption")
        image_hiding_button = QPushButton("Image Hide")
        image_reveal_button = QPushButton("Image Reveal")
        super_resolution_button = QPushButton("Super Resolution")

        # Connect button signals to their corresponding slots
        encryption_button.clicked.connect(self.show_encryption_page)
        decryption_button.clicked.connect(self.show_decryption_page)
        image_hiding_button.clicked.connect(self.show_image_hiding_page)
        image_reveal_button.clicked.connect(self.show_reveal_page)
        super_resolution_button.clicked.connect(self.show_super_resolution_page)

        # Add buttons to the side navigation layout
        side_layout.addWidget(logo_label)
        side_layout.addWidget(name_label)
        side_layout.addWidget(image_hiding_button)
        side_layout.addWidget(encryption_button)
        side_layout.addWidget(decryption_button)
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
        self.main_content = BackgroundWidget()
        self.main_content.setObjectName("main_content")
        self.main_content.set_background_image("assets/components_backgrounds/main_window_welcome_bg.png")
        self.main_layout = QVBoxLayout()
        self.main_content.setLayout(self.main_layout)

        # Add the side navigation and main content to the main window layout
        main_layout.addWidget(side_navigation)
        main_layout.addWidget(self.main_content)

        # Set the main window layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_encryption_page(self):
        self.main_content.set_background_image("assets/components_backgrounds/main_window_bg.png")
        self.image_tobe_enc_filepath = None
        self.key_text_box = None
        self.enc_img_text_label =None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>Image Encryption</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # label layout
        label_layout = QHBoxLayout()

        method_text_label = QLabel("Select encryption method:")
        method_text_label.setAlignment(Qt.AlignVCenter)
        method_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(method_text_label)

        self.enc_img_text_label = QLabel("Select Image to be Encrypted:")
        self.enc_img_text_label.setAlignment(Qt.AlignCenter)
        self.enc_img_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(self.enc_img_text_label)

        label_layout_widget = QWidget()
        label_layout_widget.setLayout(label_layout)
        self.main_layout.addWidget(label_layout_widget)

        # Image  display layout
        image_display_layout = QHBoxLayout()

        radio_layout = QVBoxLayout()
        radio_layout.setAlignment(Qt.AlignLeft)
        self.aes_radio = QRadioButton("AES Encryption")
        self.aes_radio.setStyleSheet("font-size: 16px; color: #fae69e; font-weight: bold;")
        self.blowfish_radio = QRadioButton("Blowfish Encryption")
        self.blowfish_radio.setStyleSheet("font-size: 16px; color: #fae69e; font-weight: bold;")
        encryption_group = QButtonGroup()
        encryption_group.addButton(self.aes_radio)
        encryption_group.addButton(self.blowfish_radio)
        radio_layout.addWidget(self.blowfish_radio)
        radio_layout.addWidget(self.aes_radio)

        key_text_label = QLabel("<br><br><br>Enter the secret key")
        key_text_label.setStyleSheet("font-size: 18px; color: #ffffff; font-weight: bold;")
        radio_layout.addWidget(key_text_label)

        self.key_text_box = CustomTextBox()
        self.key_text_box.setFixedWidth(300)
        radio_layout.addWidget(self.key_text_box)

        radio_layout_widget = QWidget()
        radio_layout_widget.setLayout(radio_layout)
        image_display_layout.addWidget(radio_layout_widget)

        self.enc_display_label = QLabel()
        self.enc_display_label.setAlignment(Qt.AlignLeft)
        pixmap = QPixmap("assets/dummy_images/image_dummy.png")
        self.enc_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
        image_display_layout.addWidget(self.enc_display_label)

        image_display_layout_widget = QWidget()
        image_display_layout_widget.setLayout(image_display_layout)
        self.main_layout.addWidget(image_display_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_encryption_page())
        button_layout.addWidget(clear_button)

        browse_enc_button = QPushButton("Browse image")
        browse_enc_button.clicked.connect(lambda: self.select_enc_image(self.enc_display_label))
        button_layout.addWidget(browse_enc_button)

        encrypt_button = QPushButton("Encrypt")
        encrypt_button.clicked.connect(lambda: self.perform_encryption(self.image_tobe_enc_filepath))
        button_layout.addWidget(encrypt_button)

        self.download_enc_button = QPushButton("Download encrypted file")
        self.download_enc_button.setEnabled(False)
        self.download_enc_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_enc_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_decryption_page(self):
        self.main_content.set_background_image("assets/components_backgrounds/main_window_bg.png")
        self.key_text_box_of_dec = None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>Image Decryption</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # label layout
        label_layout = QHBoxLayout()

        method_text_label = QLabel("Select Decryption method:")
        method_text_label.setAlignment(Qt.AlignVCenter)
        method_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(method_text_label)

        self.dec_img_text_label = QLabel("Select the file to be decrypted:")
        self.dec_img_text_label.setAlignment(Qt.AlignCenter)
        self.dec_img_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(self.dec_img_text_label)

        label_layout_widget = QWidget()
        label_layout_widget.setLayout(label_layout)
        self.main_layout.addWidget(label_layout_widget)

        # Image  display layout
        image_display_layout = QHBoxLayout()

        radio_layout = QVBoxLayout()
        radio_layout.setAlignment(Qt.AlignLeft)
        self.aes_radio_dec = QRadioButton("AES Decryption")
        self.aes_radio_dec.setStyleSheet("font-size: 16px; color: #fae69e; font-weight: bold;")
        self.blowfish_radio_dec = QRadioButton("Blowfish Decryption")
        self.blowfish_radio_dec.setStyleSheet("font-size: 16px; color: #fae69e; font-weight: bold;")
        encryption_group = QButtonGroup()
        encryption_group.addButton(self.aes_radio_dec)
        encryption_group.addButton(self.blowfish_radio_dec)
        radio_layout.addWidget(self.blowfish_radio_dec)
        radio_layout.addWidget(self.aes_radio_dec)

        key_text_label = QLabel("<br><br><br>Enter the secret key")
        key_text_label.setStyleSheet("font-size: 18px; color: #ffffff; font-weight: bold;")
        radio_layout.addWidget(key_text_label)

        self.key_text_box_of_dec = CustomTextBox()
        self.key_text_box_of_dec.setFixedWidth(300)
        radio_layout.addWidget(self.key_text_box_of_dec)

        radio_layout_widget = QWidget()
        radio_layout_widget.setLayout(radio_layout)
        image_display_layout.addWidget(radio_layout_widget)

        self.dec_display_label = QLabel()
        self.dec_display_label.setAlignment(Qt.AlignLeft)
        pixmap = QPixmap("assets/dummy_images/image_dummy.png")
        self.dec_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
        image_display_layout.addWidget(self.dec_display_label)

        image_display_layout_widget = QWidget()
        image_display_layout_widget.setLayout(image_display_layout)
        self.main_layout.addWidget(image_display_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_decryption_page())
        button_layout.addWidget(clear_button)

        browse_enc_button = QPushButton("Browse encrypted file")
        browse_enc_button.clicked.connect(lambda: self.select_dec_image(self.dec_display_label))
        button_layout.addWidget(browse_enc_button)

        decrypt_button = QPushButton("Decrypt")
        decrypt_button.clicked.connect(lambda: self.perform_decryption(self.enc_filepath))
        button_layout.addWidget(decrypt_button)

        self.download_dec_button = QPushButton("Download decrypted image")
        self.download_dec_button.setEnabled(False)
        self.download_dec_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_dec_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_image_hiding_page(self):
        self.main_content.set_background_image("assets/components_backgrounds/main_window_bg.png")
        self.secret_image_filepath = None
        self.cover_image_filepath = None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>STEGO CNN : Steganography Hide</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # STEGO CNN model path label
        model_path_label = QLabel("<h5>Model Path: InvisiCipher/app/models/DEEP_STEGO/models/hide.h5</h5>")
        model_path_label.setStyleSheet("font-size: 16px; color: #c6c6c6;")
        model_path_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(model_path_label)

        # GPU Info
        gpu_info_label = QLabel("<b><ul><li>Device: GPU:0 with 1654 MB memory</li><li>NVIDIA GeForce RTX 3050 Laptop GPU</li><li>Compute capability: 8.6</li><li>Loaded cuDNN version 8302</li></ul></b>")
        gpu_info_label.setStyleSheet("font-size: 13px; color: #fae69e;")
        gpu_info_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(gpu_info_label)

        # label layout
        label_layout = QHBoxLayout()
        cover_text_label = QLabel("Select cover image:")
        cover_text_label.setAlignment(Qt.AlignCenter)
        cover_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(cover_text_label)

        secret_text_label = QLabel("Select secret image:")
        secret_text_label.setAlignment(Qt.AlignCenter)
        secret_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(secret_text_label)

        steg_text_label = QLabel("Generated steg image:")
        steg_text_label.setAlignment(Qt.AlignCenter)
        steg_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
        label_layout.addWidget(steg_text_label)

        label_layout_widget = QWidget()
        label_layout_widget.setLayout(label_layout)
        self.main_layout.addWidget(label_layout_widget)

        # Image  display layout
        image_display_layout = QHBoxLayout()
        self.cover_display_label = QLabel()
        self.cover_display_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/dummy_images/cover_image_dummy.png")
        self.cover_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
        image_display_layout.addWidget(self.cover_display_label)

        self.secret_display_label = QLabel()
        self.secret_display_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/dummy_images/secret_image_dummy.png")
        self.secret_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
        image_display_layout.addWidget(self.secret_display_label)

        self.steg_display_label = QLabel()
        self.steg_display_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/dummy_images/steg_image_dummy.png")
        self.steg_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
        image_display_layout.addWidget(self.steg_display_label)

        image_display_layout_widget = QWidget()
        image_display_layout_widget.setLayout(image_display_layout)
        self.main_layout.addWidget(image_display_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_image_hiding_page())
        button_layout.addWidget(clear_button)

        browse_cover_button = QPushButton("Browse cover image")
        browse_cover_button.clicked.connect(lambda: self.select_cover_image(self.cover_display_label))
        button_layout.addWidget(browse_cover_button)

        browse_secret_button = QPushButton("Browse secret image")
        browse_secret_button.clicked.connect(lambda: self.select_secret_image(self.secret_display_label))
        button_layout.addWidget(browse_secret_button)

        hide_button = QPushButton("Hide")
        hide_button.clicked.connect(lambda: self.perform_hide(self.cover_image_filepath, self.secret_image_filepath))
        button_layout.addWidget(hide_button)

        self.download_steg_button = QPushButton("Download steg image")
        self.download_steg_button.setEnabled(False)
        self.download_steg_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_steg_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_reveal_page(self):
        self.main_content.set_background_image("assets/components_backgrounds/main_window_bg.png")
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>STEGO CNN : Steganography Reveal</H2>")
        title_label.setStyleSheet("font-size: 24px; color: #ffffff;")
        title_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(title_label)

        # STEGO CNN model path label
        model_path_label = QLabel("<h5>Model Path: InvisiCipher/app/models/DEEP_STEGO/models/reveal.h5</h5>")
        model_path_label.setStyleSheet("font-size: 16px; color: #c6c6c6;")
        model_path_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(model_path_label)

        # GPU Info
        gpu_info_label = QLabel("<b><ul><li>Device: GPU:0 with 1654 MB memory</li><li>NVIDIA GeForce RTX 3050 Laptop GPU</li><li>Compute capability: 8.6</li><li>Loaded cuDNN version 8302</li></ul></b>")
        gpu_info_label.setStyleSheet("font-size: 13px; color: #fae69e;")
        gpu_info_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(gpu_info_label)

        # image text layout
        image_text_layout = QHBoxLayout()
        container_text_label = QLabel("Select steg image:")
        container_text_label.setAlignment(Qt.AlignCenter)
        container_text_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        image_text_layout.addWidget(container_text_label)

        secret_out_text_label = QLabel("Revealed secret image:")
        secret_out_text_label.setAlignment(Qt.AlignCenter)
        secret_out_text_label.setStyleSheet("font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
        image_text_layout.addWidget(secret_out_text_label)

        image_text_layout_widget = QWidget()
        image_text_layout_widget.setLayout(image_text_layout)
        self.main_layout.addWidget(image_text_layout_widget)
        
        # Image display layout
        image_layout = QHBoxLayout()
        self.container_display_label = QLabel()
        self.container_display_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/dummy_images/steg_image_dummy.png")
        self.container_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
        image_layout.addWidget(self.container_display_label)
        
        self.secret_out_display_label = QLabel()
        self.secret_out_display_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/dummy_images/secret_image_dummy.png")
        self.secret_out_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
        image_layout.addWidget(self.secret_out_display_label)

        image_layout_widget = QWidget()
        image_layout_widget.setLayout(image_layout)
        self.main_layout.addWidget(image_layout_widget)

        # button layout
        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_reveal_page())
        button_layout.addWidget(clear_button)

        browse_cover_button = QPushButton("Browse steg image")
        browse_cover_button.clicked.connect(lambda: self.select_container_image(self.container_display_label))
        button_layout.addWidget(browse_cover_button)

        reveal_button = QPushButton("Reveal")
        reveal_button.clicked.connect(lambda: self.perform_reveal(self.container_image_filepath))
        button_layout.addWidget(reveal_button)

        self.download_revealed_secret_image_button = QPushButton("Download revealed secret image")
        self.download_revealed_secret_image_button.setEnabled(False)
        self.download_revealed_secret_image_button.clicked.connect(lambda: self.download_image())
        button_layout.addWidget(self.download_revealed_secret_image_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_layout_widget)

    def show_super_resolution_page(self):
        self.main_content.set_background_image("assets/components_backgrounds/main_window_bg.png")
        self.low_res_image_filepath = None
        # Clear the main window layout
        self.clear_main_layout()

        # Add content to the super resolution page
        title_label = QLabel("<H2>Enhanced Super Resolution using ESRGAN</H2>")
        title_label.setAlignment(Qt.AlignTop)
        title_label.setStyleSheet("font-size: 24px; color: #ffffff; margin-bottom: 20px;")
        self.main_layout.addWidget(title_label)

        # ESRGAN model path label
        model_path_label = QLabel("<h5>Model Path: InvisiCipher/app/models/ESRGAN/models/RRDB_ESRGAN_x4.pth</h5>")
        model_path_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 20px;")
        model_path_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(model_path_label)

        # GPU Info
        gpu_info_label = QLabel(
            "<b><ul><li>Device: GPU:0 with 1654 MB memory</li><li>NVIDIA GeForce RTX 3050 Laptop GPU</li><li>Compute capability: 8.6</li><li>Loaded cuDNN version 8302</li></ul></b>")
        gpu_info_label.setStyleSheet("font-size: 13px; color: #fae69e;")
        gpu_info_label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(gpu_info_label)

        # Low resolution image selection
        low_res_label = QLabel("Select Low Resolution Image:")
        low_res_label.setAlignment(Qt.AlignCenter)
        low_res_label.setStyleSheet("font-size: 16px; color: #c6c6c6; margin-bottom: 10px; font-weight: bold;")
        self.main_layout.addWidget(low_res_label)

        # image display
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/dummy_images/lr_image_dummy.png")
        image_label.setPixmap(pixmap.scaled(384, 384, Qt.KeepAspectRatio))
        self.main_layout.addWidget(image_label)

        # defining button layout
        button_layout = QHBoxLayout()

        # Browse button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(lambda: self.show_super_resolution_page())
        button_layout.addWidget(clear_button)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.select_low_resolution_image(image_label))
        button_layout.addWidget(browse_button)

        # Up-scale button
        upscale_button = QPushButton("UP-SCALE")
        upscale_button.clicked.connect(lambda: self.upscaleImage(image_label))
        button_layout.addWidget(upscale_button)

        # Download button
        download_button = QPushButton("Download")
        download_button.setObjectName("download_button")
        download_button.setEnabled(False)
        download_button.clicked.connect(self.download_image)
        button_layout.addWidget(download_button)

        # add the button layout to the main layout
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        self.main_layout.addWidget(button_widget)

        # Set the image labels as attributes
        self.low_res_image_text_label = low_res_label
        self.image_label = image_label
        self.download_HR_button = download_button

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
            self.low_res_image_text_label.setStyleSheet(
                "font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
            self.download_HR_button.setEnabled(True)
        else:
            QMessageBox.critical(self, "Upscaling Error", "Failed to upscale the image.")

    def download_image(self):
        # Implement the logic to download the high resolution image
        QMessageBox.information(self, "Download", "Downloaded the image...")

    def clear_main_layout(self):
        # Remove all widgets from the main layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def select_cover_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select cover Image")
        if filepath:
            self.cover_image_filepath = filepath
            pixmap = QPixmap(filepath)
            label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))

    def select_secret_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select secret Image")
        if filepath:
            self.secret_image_filepath = filepath
            pixmap = QPixmap(filepath)
            label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))

    def select_container_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select secret Image")
        if filepath:
            self.container_image_filepath = filepath
            pixmap = QPixmap(filepath)
            label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))

    def select_enc_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select Image")
        if filepath:
            self.image_tobe_enc_filepath = filepath
            pixmap = QPixmap(filepath)
            label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))

    def select_dec_image(self, label):
        file_dialog = QFileDialog()
        filepath, _ = file_dialog.getOpenFileName(self, "Select enc file")
        if filepath:
            self.enc_filepath = filepath
            pixmap = QPixmap("assets/dummy_images/locked_image_dummy.png")
            label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))

    def perform_hide(self, cover_filepath, secret_filepath):
        if cover_filepath is None or secret_filepath is None:
            QMessageBox.information(self, "Hiding Error", "Please select the images first.")
            return
        try:
            hide_image(cover_filepath, secret_filepath)
            steg_image_path = 'C:/Users/asirw/PycharmProjects/InvisiCipher/app/steg_image.png'
            pixmap = QPixmap(steg_image_path)
            self.steg_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
            self.download_steg_button.setEnabled(True)
        except:
            QMessageBox.critical(self, "Hiding Error", "Failed to hide the image.")

    def perform_reveal(self, filepath):
        if filepath is None:
            QMessageBox.information(self, "Revealing Error", "Please select the image first.")
            return
        try:
            reveal_image(filepath)
            secret_out_filepath = "C:/Users/asirw/PycharmProjects/InvisiCipher/app/secret_out.png"
            pixmap = QPixmap(secret_out_filepath)
            self.secret_out_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
            self.download_revealed_secret_image_button.setEnabled(True)
        except:
            QMessageBox.critical(self, "Revealing error", "Failed to reveal the image")

    def perform_encryption(self, filepath):
        if filepath is None:
            QMessageBox.information(self, "Encrypting Error", "Please select the image first.")
            return
        if not self.aes_radio.isChecked() and not self.blowfish_radio.isChecked():
            QMessageBox.information(self, "Encrypting Error", "Please select an encryption method.")
            return
        if self.key_text_box.text() == "":
            QMessageBox.information(self, "Encrypting Error", "Please enter a secret key")
            return
        try:
            if self.aes_radio.isChecked():
                aes.encrypt(filepath, self.key_text_box.text())
            else:
                blowfish.encrypt(filepath, self.key_text_box.text())
            self.download_enc_button.setEnabled(True)
            self.enc_img_text_label.setText("Encrypted!")
            self.enc_img_text_label.setStyleSheet(
                "font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
            pixmap = QPixmap("assets/dummy_images/locked_image_dummy.png")
            self.enc_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
            self.key_text_box.setText("")
        except:
            QMessageBox.critical(self, "Encrypting error", "Failed to encryp the image")

    def perform_decryption(self, filepath):
        dec_filename = None
        if filepath is None:
            QMessageBox.information(self, "Decrypting Error", "Please select the image first.")
            return
        if not self.aes_radio_dec.isChecked() and not self.blowfish_radio_dec.isChecked():
            QMessageBox.information(self, "Decrypting Error", "Please select an decryption method.")
            return
        if self.key_text_box_of_dec.text() == "":
            QMessageBox.information(self, "Decrypting Error", "Please enter a secret key")
            return
        try:
            if self.aes_radio_dec.isChecked():
                result, dec_filename = aes.decrypt(filepath, self.key_text_box_of_dec.text())
                if result == -1:
                    QMessageBox.critical(self, "Decrypting error", "Wrong Key!                   ")
                    return
            else:
                result, dec_filename = blowfish.decrypt(filepath, self.key_text_box_of_dec.text())
                if result == -1:
                    QMessageBox.critical(self, "Decrypting error", "Wrong Key!                    ")
                    return
            self.download_dec_button.setEnabled(True)
            self.dec_img_text_label.setText("Decrypted!")
            self.dec_img_text_label.setStyleSheet(
                "font-size: 16px; color: #00ff00; margin-bottom: 10px; font-weight: bold;")
            pixmap = QPixmap(dec_filename)
            self.dec_display_label.setPixmap(pixmap.scaled(256, 256, Qt.KeepAspectRatio))
            self.key_text_box_of_dec.setText("")
        except:
            QMessageBox.critical(self, "Decrypting error", "Failed to decrypt the file")

    def logout(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Logout")
        dialog.setMinimumSize(450, 100)

        layout = QVBoxLayout(dialog)
        msg_box = QMessageBox()
        msg_box.setText("<h3>Are you sure you want to logout?</h3>")

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
        stylesheet = QFile("styles/style.qss")
        if stylesheet.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(stylesheet)
            self.setStyleSheet(stream.readAll())


# Create the application
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
window = MainAppWindow()
window.load_stylesheet()
window.show()
sys.exit(app.exec_())
