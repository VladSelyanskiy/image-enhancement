import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QSlider,
    QSpinBox,
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QComboBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

import cv2
from core import ImageHandler


class ImageTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.file_name = None

        # Create image display label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 150)
        self.image_label.setStyleSheet("border: 1px solid black")

        # Create buttons
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Image")
        self.capture_btn = QPushButton("Process Image")
        self.clear_btn = QPushButton("Clear")

        # Connect buttons to functions
        self.load_btn.clicked.connect(self.load_image)
        self.capture_btn.clicked.connect(self.capture_image)
        self.clear_btn.clicked.connect(self.clear_image)

        # Add widgets to layout
        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.capture_btn)
        btn_layout.addWidget(self.clear_btn)

        # Add layout with fast choice
        choice_layout = QHBoxLayout()
        choice_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.choice_label = QLabel("Quick selection:")
        self.choice_label.setMinimumSize(50, 50)
        # Add cobmobox with different choices
        self.choice = QComboBox()
        self.choice.addItem("Remove noise")
        self.choice.addItem("Remove noise (for binary)")
        self.choice.addItem("Increase the contrast")
        # Add widgets to layout
        choice_layout.addWidget(self.choice_label)
        choice_layout.addWidget(self.choice)

        # Add widgets to main layout
        layout.addWidget(self.image_label)
        layout.addLayout(choice_layout)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio
                )
            )
        self.file_name = file_name

    def capture_image(self):
        # Placeholder for image capture functionality
        index = self.choice.currentIndex()

        handler = ImageHandler(self.file_name)

        if self.file_name is None:
            raise FileNotFoundError("No image loaded")

        image = cv2.imread(self.file_name)

        if index == 0:
            handler.makeMedianBlur(image)
        if index == 1:
            handler.delNoiseBinary(image)

    def clear_image(self):
        self.image_label.clear()
        self.image_label.setText("No image loaded")


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create settings groups
        self.create_image_settings(layout)
        self.create_processing_settings(layout)
        self.create_display_settings(layout)

        layout.addStretch()
        self.setLayout(layout)

    def create_image_settings(self, parent_layout):
        group = QGroupBox("Image Settings")
        layout = QVBoxLayout()

        # Resolution setting
        res_layout = QHBoxLayout()
        res_label = QLabel("Resolution:")
        self.resolution_spin = QSpinBox()
        self.resolution_spin.setRange(100, 2000)
        self.resolution_spin.setValue(800)
        res_layout.addWidget(res_label)
        res_layout.addWidget(self.resolution_spin)
        layout.addLayout(res_layout)

        # Quality setting
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(0, 100)
        self.quality_slider.setValue(75)
        self.quality_value = QLabel("75")
        self.quality_slider.valueChanged.connect(
            lambda v: self.quality_value.setText(str(v))
        )
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_value)
        layout.addLayout(quality_layout)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_processing_settings(self, parent_layout):
        group = QGroupBox("Processing Settings")
        layout = QVBoxLayout()

        # Processing options
        self.auto_enhance = QCheckBox("Auto Enhance")
        self.noise_reduction = QCheckBox("Noise Reduction")
        self.edge_detection = QCheckBox("Edge Detection")

        layout.addWidget(self.auto_enhance)
        layout.addWidget(self.noise_reduction)
        layout.addWidget(self.edge_detection)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_display_settings(self, parent_layout):
        group = QGroupBox("Display Settings")
        layout = QVBoxLayout()

        # Display options
        self.show_grid = QCheckBox("Show Grid")
        self.show_rulers = QCheckBox("Show Rulers")
        self.fullscreen = QCheckBox("Fullscreen Mode")

        layout.addWidget(self.show_grid)
        layout.addWidget(self.show_rulers)
        layout.addWidget(self.fullscreen)

        group.setLayout(layout)
        parent_layout.addWidget(group)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 800, 400)

        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.image_tab = ImageTab()
        self.settings_tab = SettingsTab()

        # Add tabs to widget
        self.tabs.addTab(self.image_tab, "Image")
        self.tabs.addTab(self.settings_tab, "Settings")

        # Set central widget
        self.setCentralWidget(self.tabs)


app = QApplication(sys.argv)
window = MainWindow()
