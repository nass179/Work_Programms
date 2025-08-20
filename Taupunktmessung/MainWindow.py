import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
import PyQt5.QtWidgets as qw

# Subclass QMainWindow to customize your application's main window
class ImageLabel(QLabel):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap(image_path)
        self.setScaledContents(False)  # we'll scale manually
        self.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            scaled = self.original_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)

        self.setWindowTitle("Feuchtemessung")
        self.image_label = ImageLabel("/Assets/ultratube_logo.png")
        self.button_is_checked = True
        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        #button.toggled.connect(self.button_was_toggled)
        # Set the central widget of the Window.
        #self.setCentralWidget(self.button)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label, stretch=1)  # image expands
        layout.addWidget(self.button, stretch=0)  # button stays below
        self.setLayout(layout)

    def the_button_was_clicked(self):
        self.button.setText("du hast mich schon gedrückt")
        self.button.setEnabled(False)
        print("clicked")
        self.setWindowTitle("Feuchtemessung 2")
"""
    def button_was_toggled(self, checked):
        self.button_is_checked = checked
        print("clicked?", self.button_is_checked)
"""
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
