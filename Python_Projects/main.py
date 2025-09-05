import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
                              QPushButton, QLabel, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                              QFormLayout,
                              QLineEdit, QListWidget, QMessageBox, QScrollBar, QDialog, QTextEdit
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os
#selected_baustelle = ""
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
        print("MainWindow init")

        self.selected_baustelle = ""
        self.messplatz_input = QLineEdit()
        self.projektnummer_input = QLineEdit()
        self.gasart_input = QLineEdit()
        self.beschreibung_input = QTextEdit()

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
        #self.page1.next_button.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page2))
        self.page2.next_button.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page3))
        self.page2.back_button.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page1))
        #self.page1.lb_baustellen.itemDoubleClicked.connect(lambda: self.stacked.setCurrentWidget(self.page2))
        #self.page1.btn_open.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page2))
        self.page1.lb_baustellen.itemDoubleClicked.connect(lambda: self.go_to_data_entry())
        self.page1.btn_open.clicked.connect(lambda: self.go_to_data_entry())

    def go_to_data_entry(self):
        self.page2.update_baustelle_label()
        self.stacked.setCurrentWidget(self.page2)


        

class BaustellenauswahlPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_baustelle = ""
        self.baustellen = []
        self.load_baustellen()
        self.init_ui()
        self.update_listbox()
    
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

        # Listbox
        self.lb_baustellen = QListWidget()
        self.lb_baustellen.setFont(QFont('Arial', 25))
        self.lb_baustellen.setSelectionMode(self.lb_baustellen.SingleSelection)
        self.lb_baustellen.itemClicked.connect(self.handle_item_clicked)
        layout.addWidget(self.lb_baustellen)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Ausgewählte löschen")
        btn_delete.setFont(QFont('Arial', 14))
        btn_delete.setStyleSheet("background-color: #dc3545; color: white;")
        btn_delete.clicked.connect(self.delete_baustelle)
        btn_layout.addWidget(btn_delete)

        btn_delete_all = QPushButton("Alle löschen")
        btn_delete_all.setFont(QFont('Arial', 14))
        btn_delete_all.setStyleSheet("background-color: #dc3545; color: white;")
        btn_delete_all.clicked.connect(self.delete_all)
        btn_layout.addWidget(btn_delete_all)

        self.btn_open = QPushButton("Öffnen")
        self.btn_open.setFont(QFont('Arial', 14))
        self.btn_open.setStyleSheet("background-color: #007bff; color: white;")
        #self.btn_open.clicked.connect(lambda: self.handle_item_clicked())
        btn_layout.addWidget(self.btn_open)

        layout.addLayout(btn_layout)


        layout.addLayout(entry_layout)
        self.setLayout(layout)
    
    def handle_item_clicked(self):
        selected_items = self.lb_baustellen.selectedItems()
        if selected_items:
            self.selected_baustelle = selected_items[0].text()
            self.main_window.selected_baustelle = self.selected_baustelle  # <-- update parent
            print("Selected Baustelle:", self.selected_baustelle)
            print("Main Window Selected Baustelle:", self.main_window.selected_baustelle)

    def load_tasks(self):
        try:
            with open("baustellen.txt", "r") as file:
                self.baustellen = file.read().splitlines()
        except FileNotFoundError:
            self.baustellen = []

    def save_tasks(self):
        with open("baustellen.txt", "w") as file:
            file.write("\n".join(self.baustellen))

    def update_listbox(self):
        self.lb_baustellen.clear()
        for task in self.baustellen:
            self.lb_baustellen.addItem(task)

    def add_task(self):
        task = self.txt_input.text().strip()
        if task:
            self.baustellen.append(task)
            self.update_listbox()
            self.save_tasks()
            self.txt_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Bitte geben Sie einen gültigen Baustellennamen ein.")

    def delete_baustelle(self):
        selected_items = self.lb_baustellen.selectedItems()
        if selected_items:
            task = selected_items[0].text()
            reply = QMessageBox.question(self, "Bestätigung",
                                         f"Sind Sie sicher, dass Sie die Baustelle '{task}' löschen möchten?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.baustellen.remove(task)
                self.update_listbox()
                self.save_tasks()

    def delete_all(self):
        reply = QMessageBox.question(self, "Bestätigung",
                                     "Sind Sie sicher, dass Sie alle Baustellen löschen möchten?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.baustellen.clear()
            self.update_listbox()
            self.save_tasks()
            QMessageBox.information(self, "Info", "Alle Baustellen wurden erfolgreich gelöscht.")

    def load_baustellen(self):
        if os.path.exists("baustellen.txt"):
            with open("baustellen.txt", "r") as file:
                self.baustellen = [line.strip() for line in file.readlines()]
        else:
            self.baustellen = []
        

class DataEntryPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        self.init_ui()

        

    def init_ui(self):
        layout = QVBoxLayout()
        self.next_button = QPushButton("Weiter zu DataWindow")
        #layout.addWidget(QLabel("DataEntry"))
        #layout.addWidget(self.next_button, alignment=Qt.AlignBottom)

        formlayout = QFormLayout()
        #global selected_baustelle
        print("Selected Baustelle in DataEntryPage:", self.main_window.selected_baustelle)
        self.baustelle_label = QLabel(self.main_window.selected_baustelle)  # <-- store reference!
        self.baustelle_label.setFont(QFont('Arial', 20))
        formlayout.addRow("Baustelle:", self.baustelle_label)
        self.main_window.projektnummer_input.setFont(QFont('Arial', 20))
        self.main_window.messplatz_input.setFont(QFont('Arial', 20))
        self.main_window.gasart_input.setFont(QFont('Arial', 20))
        self.main_window.beschreibung_input.setFont(QFont('Arial', 20))
        formlayout.addRow("Projektnummer:", self.main_window.projektnummer_input)
        #formlayout.addRow("Datum:", QLabel("2024-10-01"))
        formlayout.addRow("Messplatz:", self.main_window.messplatz_input)
        formlayout.addRow("Gasart:", self.main_window.gasart_input)
        formlayout.addRow("Beschreibung:", self.main_window.beschreibung_input)

        formlayout.setVerticalSpacing(20)  # Increase space between rows
        layout.addLayout(formlayout)
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("Zurück")
        self.back_button.setFont(QFont('Arial', 24))           # Larger font
        self.back_button.setMinimumSize(200, 80)               # Larger button

        self.next_button = QPushButton("Weiter zum Datenfenster")
        self.next_button.setFont(QFont('Arial', 24))           # Larger font
        self.next_button.setMinimumSize(200, 80)               # Larger button

        nav_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        nav_layout.addStretch(1)
        nav_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        layout.addLayout(nav_layout)
        
        self.setLayout(layout)

    def update_baustelle_label(self):
        # Update the Baustelle label when navigating to this page
        print("Updating Baustelle label in DataEntryPage:", self.main_window.selected_baustelle)
        # Assuming the first row is the Baustelle row
        self.baustelle_label.setText(self.main_window.selected_baustelle)
        print(self.main_window.selected_baustelle)

class DataWindowPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("DataWindow"))
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec_()