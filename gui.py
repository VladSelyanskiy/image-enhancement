from typing import Dict, Any
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
    QGroupBox,
    QHBoxLayout,
    QComboBox,
    QRadioButton,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from core import ImageHandler


class ImageTab(QWidget):
    def __init__(self, settings_tab: "SettingsTab"):
        super().__init__()
        self.settings_tab = settings_tab  # Store reference to SettingsTab
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
        self.choice.addItem("Make Equalization")
        self.choice.addItem("Increase image contrast")
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

        if self.file_name is None:
            raise FileNotFoundError("No image loaded")

        handler = ImageHandler(self.file_name, **self.settings_tab.toDict())

        if index == 0:
            handler.makeMedianBlur()
        if index == 1:
            handler.delNoiseBinary()
        if index == 2:
            handler.makeEqualization()
        if index == 3:
            handler.applyClahe()

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

        layout.addStretch()
        self.setLayout(layout)

    def create_image_settings(self, parent_layout):
        group = QGroupBox("Image Settings")
        layout = QVBoxLayout()

        res_label = QLabel("Resolution:")
        layout.addWidget(res_label)

        # Use specific resolution checkbox
        self.specific_res_checkbox = QCheckBox("Use specific resolution")
        self.specific_res_checkbox.setChecked(False)
        self.specific_res_checkbox.stateChanged.connect(self.toggle_resolution)
        layout.addWidget(self.specific_res_checkbox)

        # Resolution setting
        height_layout = QHBoxLayout()
        height_label = QLabel("Height:")
        self.height_spin = QSpinBox()
        self.height_spin.setEnabled(False)
        self.height_spin.setRange(100, 2000)
        self.height_spin.setValue(800)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_spin)
        layout.addLayout(height_layout)

        # Resolution setting
        width_layout = QHBoxLayout()
        width_label = QLabel("Weight:")
        self.width_spin = QSpinBox()
        self.width_spin.setEnabled(False)
        self.width_spin.setRange(100, 2000)
        self.width_spin.setValue(800)
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_spin)
        layout.addLayout(width_layout)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def create_processing_settings(self, parent_layout):
        group = QGroupBox("Processing Settings")
        layout = QVBoxLayout()

        # Reduction group
        reduction_layout = QVBoxLayout()
        reduction_group = QGroupBox("Reduction")

        # Reduction setting for commom cases
        reduction_layout1 = QHBoxLayout()
        reduction_label1 = QLabel("Level of reduction for common cases:")
        self.reduction_slider1 = QSlider(Qt.Orientation.Horizontal)
        self.reduction_slider1.setRange(1, 13)
        self.reduction_slider1.setValue(5)
        self.reduction_value1 = QLabel("5")
        self.reduction_slider1.valueChanged.connect(
            lambda v: self.reduction_value1.setText(str(v))
        )
        reduction_layout1.addWidget(reduction_label1)
        reduction_layout1.addWidget(self.reduction_slider1)
        reduction_layout1.addWidget(self.reduction_value1)
        reduction_layout.addLayout(reduction_layout1)

        # Reduction setting for binary cases
        reduction_layout2 = QHBoxLayout()
        reduction_label2 = QLabel("Level of reduction for binary cases:")
        self.reduction_slider2 = QSlider(Qt.Orientation.Horizontal)
        self.reduction_slider2.setRange(1, 13)
        self.reduction_slider2.setValue(5)
        self.reduction_value2 = QLabel("5")
        self.reduction_slider2.valueChanged.connect(
            lambda v: self.reduction_value2.setText(str(v))
        )
        reduction_layout2.addWidget(reduction_label2)
        reduction_layout2.addWidget(self.reduction_slider2)
        reduction_layout2.addWidget(self.reduction_value2)
        reduction_layout.addLayout(reduction_layout2)

        reduction_group.setLayout(reduction_layout)
        layout.addWidget(reduction_group)

        # Cases for binary processing
        # Create a group box to contain the radio buttons
        group_box = QGroupBox("Type of binary processing")
        group_layout = QVBoxLayout()

        self.radio1 = QRadioButton("Opening\n(Good for removing noise)")
        group_layout.addWidget(self.radio1)

        self.radio2 = QRadioButton("Closing\n(Good for filling holes)")
        group_layout.addWidget(self.radio2)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        # Cases for equalizations
        # Create a group box to contain the radio buttons
        equ_group = QGroupBox("Type of equalization")
        equ_layout = QVBoxLayout()

        self.equ_radio1 = QRadioButton("Global\n(Good for images with low contrast)")
        equ_layout.addWidget(self.equ_radio1)

        self.equ_radio2 = QRadioButton("Adaptive\n(Good for images with bright parts)")
        equ_layout.addWidget(self.equ_radio2)

        equ_group.setLayout(equ_layout)
        layout.addWidget(equ_group)

        # Contrast level setting
        contrast_group = QGroupBox("Contrast")
        contrast_layout = QHBoxLayout()
        contrast_label = QLabel("Contrast enhancement level:")
        self.contrast_spin = QSpinBox()
        self.contrast_spin.setRange(1, 10)
        self.contrast_spin.setValue(3)
        contrast_layout.addWidget(contrast_label)
        contrast_layout.addWidget(self.contrast_spin)
        contrast_group.setLayout(contrast_layout)
        layout.addWidget(contrast_group)

        group.setLayout(layout)
        parent_layout.addWidget(group)

    def toggle_resolution(self, checked):
        self.height_spin.setEnabled(checked)
        self.width_spin.setEnabled(checked)

    def toDict(self) -> Dict[str, Any]:
        return {
            "height": self.height_spin.value(),
            "width": self.width_spin.value(),
            "reduction_common": self.reduction_slider1.value(),
            "reduction_binary": self.reduction_slider2.value(),
            "opening": not (self.radio2.isChecked()),
            "global_equ": not (self.equ_radio2.isChecked()),
            "contrast": self.contrast_spin.value(),
            "resolution": self.specific_res_checkbox.isChecked(),
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 800, 400)

        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.settings_tab = SettingsTab()
        self.image_tab = ImageTab(
            settings_tab=self.settings_tab
        )  # Pass settings_tab reference

        # Add tabs to widget
        self.tabs.addTab(self.image_tab, "Image")
        self.tabs.addTab(self.settings_tab, "Settings")

        # Set central widget
        self.setCentralWidget(self.tabs)


app = QApplication(sys.argv)
window = MainWindow()
