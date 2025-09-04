import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
                              QPushButton, QLabel, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                              QLineEdit, QListWidget, QMessageBox, QScrollBar, QDialog, QTextEdit
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap("ultratube_logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        btn_start = QPushButton("Start")
        btn_start.setFont(QFont('Arial', 40))
        layout.addWidget(btn_start, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.btn_start = btn_start  # Expose for connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Feuchtemessung")
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        self.home_page = HomePage(self)
        self.page1 = BaustellenauswahlPage(self)
        self.page2 = DataEntryPage(self)
        self.page3 = DataWindowPage(self)

        self.stacked.addWidget(self.home_page)
        self.stacked.addWidget(self.page1)
        self.stacked.addWidget(self.page2)
        self.stacked.addWidget(self.page3)

        self.home_page.btn_start.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page1))
        self.page1.next_button.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page2))
        self.page2.next_button.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page3))

class BaustellenauswahlPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.baustellen = []
        self.load_baustellen()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Baustellenauswahl")
        title.setFont(QFont("Helvetica", 40, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.next_button = QPushButton("Weiter zu DataEntry")
        layout.addWidget(self.next_button)

        entry_layout = QHBoxLayout()
        entry_label = QLabel("Neue Baustelle:")
        entry_label.setFont(QFont('Arial', 20))
        entry_layout.addWidget(entry_label)

        self.txt_input = QLineEdit()
        self.txt_input.setFont(QFont('Arial', 20))
        self.txt_input.setFixedWidth(600)
        self.txt_input.returnPressed.connect(self.add_task)
        entry_layout.addWidget(self.txt_input)

        btn_add_task = QPushButton("Hinzufügen")
        btn_add_task.setFont(QFont('Arial', 25))
        btn_add_task.setStyleSheet("background-color: #007bff; color: white;")
        btn_add_task.clicked.connect(self.add_task)
        entry_layout.addWidget(btn_add_task)

        layout.addLayout(entry_layout)
        self.setLayout(layout)

    def load_tasks(self):
        try:
            with open("baustellen.txt", "r") as file:
                self.tasks = file.read().splitlines()
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open("baustellen.txt", "w") as file:
            file.write("\n".join(self.tasks))

    def update_listbox(self):
        self.lb_tasks.clear()
        for task in self.tasks:
            self.lb_tasks.addItem(task)

    def add_task(self):
        task = self.txt_input.text().strip()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            self.save_tasks()
            self.txt_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Bitte geben Sie einen gültigen Baustellennamen ein.")







    def load_baustellen(self):
        if os.path.exists("baustellen.txt"):
            with open("baustellen.txt", "r") as file:
                self.baustellen = [line.strip() for line in file.readlines()]
        else:
            self.baustellen = []
        




        
        

class DataEntryPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        self.next_button = QPushButton("Weiter zu DataWindow")
        layout.addWidget(QLabel("DataEntry"))
        layout.addWidget(self.next_button)
        self.setLayout(layout)

class DataWindowPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("DataWindow"))
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()