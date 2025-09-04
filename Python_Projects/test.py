import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QMessageBox, QScrollBar, QDialog, QTextEdit
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os

selected_baustelle = ""
messplatz = ""
projektnummer = ""
gasart = ""
beschreibung = ""

class ModbusRTUClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ModbusRTUClient")
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("ultratube_logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Start button
        btn_start = QPushButton("Start")
        btn_start.setFont(QFont('Arial', 40))
        btn_start.clicked.connect(self.open_baustellenauswahl)
        layout.addWidget(btn_start, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def open_baustellenauswahl(self):
        self.hide()
        self.baustellenauswahl_window = Baustellenauswahl(self)
        self.baustellenauswahl_window.show()

class Baustellenauswahl(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Baustellenauswahl')
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.tasks = []
        self.load_tasks()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Baustellenauswahl")
        title.setFont(QFont("Helvetica", 40, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Task Entry
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

        main_layout.addLayout(entry_layout)

        # Listbox
        self.lb_tasks = QListWidget()
        self.lb_tasks.setFont(QFont('Arial', 25))
        self.lb_tasks.setSelectionMode(self.lb_tasks.SingleSelection)
        self.lb_tasks.itemDoubleClicked.connect(self.on_double_click)
        main_layout.addWidget(self.lb_tasks)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Ausgewählte löschen")
        btn_delete.setFont(QFont('Arial', 14))
        btn_delete.setStyleSheet("background-color: #dc3545; color: white;")
        btn_delete.clicked.connect(self.delete_task)
        btn_layout.addWidget(btn_delete)

        btn_delete_all = QPushButton("Alle löschen")
        btn_delete_all.setFont(QFont('Arial', 14))
        btn_delete_all.setStyleSheet("background-color: #dc3545; color: white;")
        btn_delete_all.clicked.connect(self.delete_all)
        btn_layout.addWidget(btn_delete_all)

        btn_open = QPushButton("Öffnen")
        btn_open.setFont(QFont('Arial', 14))
        btn_open.setStyleSheet("background-color: #007bff; color: white;")
        btn_open.clicked.connect(self.open_data_entry_app)
        btn_layout.addWidget(btn_open)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.update_listbox()

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

    def delete_task(self):
        selected_items = self.lb_tasks.selectedItems()
        if selected_items:
            task = selected_items[0].text()
            reply = QMessageBox.question(self, "Bestätigung",
                                         f"Sind Sie sicher, dass Sie die Baustelle '{task}' löschen möchten?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.tasks.remove(task)
                self.update_listbox()
                self.save_tasks()

    def delete_all(self):
        reply = QMessageBox.question(self, "Bestätigung",
                                     "Sind Sie sicher, dass Sie alle Baustellen löschen möchten?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tasks.clear()
            self.update_listbox()
            self.save_tasks()
            QMessageBox.information(self, "Info", "Alle Baustellen wurden erfolgreich gelöscht.")

    def open_data_entry_app(self):
        selected_items = self.lb_tasks.selectedItems()
        if selected_items:
            global selected_baustelle
            selected_baustelle = selected_items[0].text()
            self.hide()
            # DataEntryApp()  # Implement this class similarly in PyQt5

    def on_double_click(self, item):
        print(f"Double-clicked on: {item.text()}")
        self.open_data_entry_app()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModbusRTUClientApp()
    window.show()
    sys.exit(app.exec_())