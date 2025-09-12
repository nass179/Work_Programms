import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
                              QPushButton, QLabel, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                              QFormLayout,
                              QLineEdit, QListWidget, QMessageBox, QScrollBar, QDialog, QTextEdit, QTextBrowser
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os

import serial.tools.list_ports
import Modbus_Communication as Mc
import os
import Calc
import xlsxwriter
import pandas as pd
import subprocess

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
        self.messplatz_input.setPlaceholderText("MP1")
        self.projektnummer_input = QLineEdit()
        self.projektnummer_input.setPlaceholderText("P25-001")
        self.gasart_input = QLineEdit()
        self.gasart_input.setPlaceholderText("N2")
        self.beschreibung_input = QTextEdit()
        self.beschreibung_input.setPlaceholderText("Hier Beschreibung eingeben...")

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
        self.page2.next_button.clicked.connect(lambda: self.go_to_data_window())
        #self.page2.next_button.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page3))
        self.page2.back_button.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page1))
        #self.page1.lb_baustellen.itemDoubleClicked.connect(lambda: self.stacked.setCurrentWidget(self.page2))
        #self.page1.btn_open.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page2))
        self.page1.lb_baustellen.itemDoubleClicked.connect(lambda: self.go_to_data_entry())
        self.page1.btn_open.clicked.connect(lambda: self.go_to_data_entry())

        self.page3.back_button2.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page2))

    def go_to_data_entry(self):
        self.page2.update_baustelle_label()
        self.stacked.setCurrentWidget(self.page2)

    # goes to datawindow if all confirmations are yes
    def go_to_data_window(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Bestätigung")
        msg.setText(
            f"Haben Sie alle Daten korrekt eingegeben?\n\n"
            f"Baustelle: {self.selected_baustelle}\n"
            f"Projektnummer: {self.projektnummer_input.text()}\n"
            f"Messplatz: {self.messplatz_input.text()}\n"
            f"Gasart: {self.gasart_input.text()}\n"
            f"Beschreibung: {self.beschreibung_input.toPlainText()}"
        )
        msg.setFont(QFont('Arial', 24))
        msg.setIcon(QMessageBox.Question)
        yes_btn = msg.addButton("Ja", QMessageBox.YesRole)
        no_btn = msg.addButton("Nein", QMessageBox.NoRole)
        yes_btn.setFont(QFont('Arial', 20))
        no_btn.setFont(QFont('Arial', 20))
        msg.exec_()
        if msg.clickedButton() == yes_btn:
            # Second confirmation
            msg2 = QMessageBox(self)
            msg2.setWindowTitle("Bestätigung")
            msg2.setText("Haben Sie das Kabel an den Sensor angeschlossen?")
            msg2.setFont(QFont('Arial', 24))
            msg2.setIcon(QMessageBox.Question)
            yes_btn2 = msg2.addButton("Ja", QMessageBox.YesRole)
            no_btn2 = msg2.addButton("Nein", QMessageBox.NoRole)
            yes_btn2.setFont(QFont('Arial', 20))
            no_btn2.setFont(QFont('Arial', 20))
            msg2.exec_()
            if msg2.clickedButton() == yes_btn2:
                # Third confirmation
                msg3 = QMessageBox(self)
                msg3.setWindowTitle("Bestätigung")
                msg3.setText("Wird das Rohr durchflossen?")
                msg3.setFont(QFont('Arial', 24))
                msg3.setIcon(QMessageBox.Question)
                yes_btn3 = msg3.addButton("Ja", QMessageBox.YesRole)
                no_btn3 = msg3.addButton("Nein", QMessageBox.NoRole)
                yes_btn3.setFont(QFont('Arial', 20))
                no_btn3.setFont(QFont('Arial', 20))
                msg3.exec_()
                if msg3.clickedButton() == yes_btn3:
                    self.stacked.setCurrentWidget(self.page3)
                else:
                    self.show_large_warning("Bitte stellen Sie sicher, dass das Rohr durchflossen wird.")
                    #QMessageBox.warning(self, "Warning", "Bitte stellen Sie sicher, dass das Rohr durchflossen wird.")
            else:
                self.show_large_warning("Bitte schließen Sie das Kabel an den Sensor an.")
                #QMessageBox.warning(self, "Warning", "Bitte schließen Sie das Kabel an den Sensor an.")

    def show_large_warning(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Warnung")
        msg.setText(message)
        msg.setFont(QFont('Arial', 24))  # Large font for text
        msg.setIcon(QMessageBox.Warning)
        ok_btn = msg.addButton("OK", QMessageBox.AcceptRole)
        ok_btn.setFont(QFont('Arial', 20))  # Large font for button
        msg.exec_()

'''
======================================================================================
=====================Baustellenauswahl Page========================================================
======================================================================================
'''
        

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

        entry_layout = QHBoxLayout()
        entry_label = QLabel("Neue Baustelle:")
        entry_label.setFont(QFont('Arial', 30))
        entry_layout.addWidget(entry_label)

        self.txt_input = QLineEdit()
        self.txt_input.setFont(QFont('Arial', 30))
        #self.txt_input.setFixedWidth(600)
        self.txt_input.returnPressed.connect(self.add_task)
        entry_layout.addWidget(self.txt_input)

        btn_add_task = QPushButton("Hinzufügen")
        btn_add_task.setFont(QFont('Arial', 30))
        btn_add_task.setStyleSheet("background-color: #007bff; color: white;")
        btn_add_task.setMinimumSize(400, 80)
        btn_add_task.clicked.connect(self.add_task)
        entry_layout.addWidget(btn_add_task)

        # Listbox
        list_layout = QVBoxLayout()
        self.lb_baustellen = QListWidget()
        self.lb_baustellen.setFont(QFont('Arial', 30))
        self.lb_baustellen.setSelectionMode(self.lb_baustellen.SingleSelection)
        self.lb_baustellen.itemClicked.connect(self.handle_item_clicked)
        list_layout.addWidget(self.lb_baustellen)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Ausgewählte löschen")
        btn_delete.setFont(QFont('Arial', 30))
        btn_delete.setStyleSheet("background-color: #dc3545; color: white;")
        btn_delete.setMinimumHeight(80)
        btn_delete.clicked.connect(self.delete_baustelle)
        btn_layout.addWidget(btn_delete)

        btn_delete_all = QPushButton("Alle löschen")
        btn_delete_all.setFont(QFont('Arial', 30))
        btn_delete_all.setStyleSheet("background-color: #dc3545; color: white;")
        btn_delete_all.setMinimumHeight(80)
        btn_delete_all.clicked.connect(self.delete_all)
        btn_layout.addWidget(btn_delete_all)

        self.btn_open = QPushButton("Öffnen")
        self.btn_open.setFont(QFont('Arial', 30))
        self.btn_open.setMinimumHeight(80)
        self.btn_open.setStyleSheet("background-color: #007bff; color: white;")
        #self.btn_open.clicked.connect(lambda: self.handle_item_clicked())

        btn_layout.addWidget(self.btn_open)

        layout.addLayout(entry_layout)
        layout.addLayout(list_layout)
        layout.addLayout(btn_layout)
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
    
'''
======================================================================================
=====================Data Entry Page========================================================
======================================================================================
'''
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
        self.back_button.setStyleSheet("background-color: #dc3545; color: white;")

        self.next_button = QPushButton("Weiter zum Datenfenster")
        self.next_button.setFont(QFont('Arial', 24))           # Larger font
        self.next_button.setMinimumSize(200, 80)               # Larger button
        self.next_button.setStyleSheet("background-color: #007bff; color: white;")

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

'''
======================================================================================
=====================Data Window Page========================================================  
======================================================================================
'''
class DataWindowPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer_running = False

    def init_ui(self):
        layout = QVBoxLayout()
        self.back_button2 = QPushButton("Zurück")
        self.back_button2.setFont(QFont('Arial', 24))           # Larger font
        self.back_button2.setMinimumSize(200, 80)  
        self.back_button2.setStyleSheet("background-color: #dc3545; color: white;")
        layout.addWidget(self.back_button2, stretch=1)

        title_label = QLabel("Datenfenster")
        title_label.setFont(QFont('Arial', 32))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.tau_label = QLabel("Taupunkt: 0 °C")
        self.tau_label.setFont(QFont('Arial', 24))
        self.tau_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.tau_label)

        self.humidity_label = QLabel("Relative Feuchtigkeit: 0 %rH")
        self.humidity_label.setFont(QFont('Arial', 24))
        self.humidity_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.humidity_label)
        '''
        self.pressure_label = QLabel("Druck: 0 bar")
        self.pressure_label.setFont(QFont('Arial', 24))
        self.pressure_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pressure_label)
        '''
        self.temperature_label = QLabel("Temperatur: 0 °C")
        self.temperature_label.setFont(QFont('Arial', 24))
        self.temperature_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.temperature_label)

        self.abs_hum_label = QLabel("Abs. Feuchtigkeit 0 g/m³")
        self.abs_hum_label.setFont(QFont('Arial', 24))
        self.abs_hum_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.abs_hum_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_read = QPushButton("Lesen")
        self.btn_read.setFont(QFont('Arial', 24))
        self.btn_read.setMinimumSize(200, 80)
        self.btn_read.setStyleSheet("background-color: #007bff; color: white;")
        self.btn_read.clicked.connect(self.start_timer_and_update)
        btn_layout.addWidget(self.btn_read)

        self.btn_dokumentieren = QPushButton("Dokumentieren")
        self.btn_dokumentieren.setFont(QFont('Arial', 24))
        self.btn_dokumentieren.setMinimumSize(200, 80)
        self.btn_dokumentieren.setStyleSheet("background-color: #28a745; color: white;")
        self.btn_dokumentieren.clicked.connect(self.create_file)
        btn_layout.addWidget(self.btn_dokumentieren)
        
        self.btn_preview = QPushButton("Vorschau")
        self.btn_preview.setFont(QFont('Arial', 24))
        self.btn_preview.setMinimumSize(200, 80)
        self.btn_preview.setStyleSheet("background-color: #ffc107; color: black;")
        self.btn_preview.clicked.connect(self.show_pdf_preview)
        btn_layout.addWidget(self.btn_preview)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    

    def start_timer_and_update(self):
        self.update_labels()  # Einmal sofort aktualisieren
        if not self.timer_running:
            self.timer.start(1000)  # Startet den Timer
            self.timer_running = True
    
    def update_labels(self):
        ports = serial.tools.list_ports.comports()
        com_port = "/dev/ttyUSB0" # ttyUSB0 for Linux
        for port in ports:
            if "USB Serial Port" in port.description:
                com_port = port.device
        self.data = Mc.client(com_port, 19200, 3, 2, 2301, 8, 'd7af')
        abs_humid = Calc.absolute_humidity(float(str(self.data[1])), float(str(self.data[3])))

        self.tau_label.setText(f"Taupunkt: {self.data[0]} °C")
        self.humidity_label.setText(f"Relative Feuchtigkeit: {float(self.data[1])} %rH")
        #self.pressure_label.setText(f"Druck: {self.data[2]} bar")
        self.temperature_label.setText(f"Temperatur: {self.data[3]} °C")
        self.abs_hum_label.setText(f"Abs. Feuchtigkeit {abs_humid:.2f} g/m³")

    def create_file(self):
        try:
            abs_humid = Calc.absolute_humidity(float(str(self.data[1])), float(str(self.data[3])))
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            print(desktop_path)
            baustelle = self.main_window.selected_baustelle.replace(" ", "")
            messplatz = self.main_window.messplatz_input.text().replace(" ", "")
            output_filename = (
                f"{baustelle}_{messplatz}.xlsx"
            )
            output_filepath = os.path.join(desktop_path, output_filename)
            workbook = xlsxwriter.Workbook(output_filepath)
            worksheet = workbook.add_worksheet()
            worksheet.set_paper(9)
            worksheet.set_margins(top=0, bottom=0, left=0, right=0)
            img_path = 'Briefbogen Aktuell 2021.png'
            worksheet.set_column("A:F", 15.4)
            worksheet.insert_image('A1', img_path, {'x_scale': 0.7, 'y_scale': 0.8, 'x_offset': 0, 'y_offset': 0})
            
            print(self.main_window.selected_baustelle + " " + "Baustelle")
            print(self.main_window.projektnummer_input.text() + " " + "Projektnummer")
            print(self.main_window.messplatz_input.text()+ " " + "Messplatz")
            print(self.main_window.gasart_input.text()+ " " + "Gasart")
            print(self.main_window.beschreibung_input.toPlainText()+ " " + "Beschreibung")

            cell_format = workbook.add_format({'font_size': 8})
            worksheet.write("B16", "Prüfauftrag: Feuchtemessung")
            worksheet.write("B17", "Projektnummer: " + self.main_window.projektnummer_input.text())
            worksheet.write("D16", "Baustelle:" + self.main_window.selected_baustelle)
            worksheet.write("B19", "Sensor: S220")
            worksheet.write("D19", "Gasart: " + self.main_window.gasart_input.text())
            worksheet.write("E19", "Messplatz: " + self.main_window.messplatz_input.text())
            worksheet.add_table('B20:E23', {'header_row': False})
            table_values = [
                ["Messgrößen: ", "Absolute Feuchtigkeit", "Relative Feuchtigkeit", "Taupunkt"],
                ["Einheit: ", "g/m³", "%rH", "°C Td"],
                ["", f"{abs_humid:.2f}", str(self.data[1]), str(self.data[0]), str(self.data[3])]
            ]

            for i in range(len(table_values[0])):
                worksheet.write(f"B{i + 20}", table_values[0][i])
                worksheet.write(f"D{i + 20}", table_values[1][i])
                worksheet.write(f"E{i + 20}", table_values[2][i])
            
            worksheet.write("B25", "MP1: " + self.main_window.messplatz_input.text())
            worksheet.write("B26", "Prüfausdruck Nr.: 1")
            worksheet.write("B27", "Beschreibung: " + self.main_window.beschreibung_input.toPlainText())
            worksheet.write(
                "B50",
                "Messbereich: -100 ... +20 °C Td   Genauigkeit: ± 1 °C Td (0 ... 20 °C Td); ± 2 °C Td ("
                "-60 ... 0 °C Td); ± 3 °C (-100 ... -60 °C Td)",
                cell_format
            )
            workbook.close()
            pdf_path = output_filepath.replace('.xlsx', '.pdf')
            self.excel_to_pdf(output_filepath, pdf_path)
            # PyQt5 message box
            msg = QMessageBox(self)
            msg.setWindowTitle("Info")
            msg.setText("Daten erfolgreich dokumentiert!\nDokument ist auf dem Desktop gespeichert!")
            msg.setFont(QFont('Arial', 24))
            ok_btn = msg.addButton("OK", QMessageBox.AcceptRole)
            ok_btn.setFont(QFont('Arial', 20))
            msg.exec_()
        except (ValueError, AttributeError) as e:
            print(e)
            msg = QMessageBox(self)
            msg.setWindowTitle("Information")
            msg.setText("Fehler! Drück die Lesen Taste und versicher dich das die Daten gelesen werden vor dem Dokumentieren!")
            msg.setFont(QFont('Arial', 24))
            ok_btn = msg.addButton("OK", QMessageBox.AcceptRole)
            ok_btn.setFont(QFont('Arial', 20))
            msg.exec_()
    

    def excel_to_pdf(self, excel_path, pdf_path):
    # LibreOffice must be installed!
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", os.path.dirname(pdf_path),
            excel_path
        ])

    def show_pdf_preview(self):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        baustelle = self.main_window.selected_baustelle.replace(" ", "")
        messplatz = self.main_window.messplatz_input.text().replace(" ", "")
        pdf_name = (
            f"{baustelle}_{messplatz}.pdf"
        )
        print("PDF name:", pdf_name)
        pdf_path = os.path.join(desktop_path, pdf_name)
        os.system("xdg-open " + pdf_path) 
        '''
        print("PDF path:", pdf_path)
        print("PDF exists:", os.path.exists(pdf_path))
        print("PDF size:", os.path.getsize(pdf_path) if os.path.exists(pdf_path) else "File not found")
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("PDF-Vorschau")
        preview_dialog.resize(900, 600)
        layout = QVBoxLayout()
        pdf_view = QWebEngineView()
        pdf_view.load(QUrl.fromLocalFile(pdf_path))
        layout.addWidget(pdf_view)
        btn_close = QPushButton("Schließen")
        btn_close.setFont(QFont('Arial', 20))
        btn_close.clicked.connect(preview_dialog.accept)
        layout.addWidget(btn_close)
        preview_dialog.setLayout(layout)
        preview_dialog.exec_()
        '''

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.showMaximized()
    app.exec_()