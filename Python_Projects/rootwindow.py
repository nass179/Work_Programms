import serial.tools.list_ports
import tkinter as tk
import tkinter.messagebox as messagebox
import Modbus_Communication as Mc
import os
import Calc
import xlsxwriter

global selected_baustelle
global messplatz
global projektnummer
global gasart
global beschreibung


class ModbusRTUClientApp:
    def __init__(self, root):
        self.root = root
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height - 80}+0+0")
        self.root.wm_attributes("-topmost", True)

        self.root.title("ModbusRTUClient")
        self.baustellenauswahl_window = None

        self.logo = tk.PhotoImage(file="ultratube_logo.png")
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")

        # Logo
        self.image_label = tk.Label(self.main_frame, image=self.logo)
        self.image_label.image = self.logo  # Keep a reference to the image
        self.image_label.pack(pady=10)

        # Start button
        btn_start = tk.Button(self.main_frame, text="Start", font=('Arial', 18), command=self.open_baustellenauswahl)
        btn_start.pack(pady=10)

    def open_baustellenauswahl(self):
        self.root.withdraw()  # Hide root window
        self.baustellenauswahl_window = tk.Toplevel(self.root)
        Baustellenauswahl(self.baustellenauswahl_window)


class Baustellenauswahl:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='lightgrey')
        self.root.title('Baustellenauswahl')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the geometry to fullscreen windowed mode
        self.root.geometry(f"{screen_width}x{screen_height - 80}+0+0")
        self.root.wm_attributes("-topmost", True)

        self.tasks = []
        self.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = tk.Label(self.root, text="Baustellenauswahl", bg='lightgrey', font=("Helvetica", 20, "bold"))
        self.title.pack(pady=(20, 10))

        # Task Entry
        self.txt_input_frame = tk.Frame(self.root, bg='lightgrey')
        self.txt_input_frame.pack(pady=(10, 20))

        self.txt_input_label = tk.Label(self.txt_input_frame, text="Neue Baustelle:", bg='lightgrey',
                                        font=('Arial', 14))
        self.txt_input_label.pack(side="left", padx=(10, 5))

        self.txt_input = tk.Entry(self.txt_input_frame, width=50, font=('Arial', 14))
        self.txt_input.pack(side="left", padx=5, pady=5)
        self.txt_input.bind('<Return>', self.add_task)  # Bind Enter key to add_task function

        self.btn_add_task = tk.Button(self.txt_input_frame, text="Hinzufügen", fg='white', bg='#007bff',
                                      font=('Arial', 14), command=self.add_task)
        self.btn_add_task.pack(side="left", padx=(5, 10))

        # Listbox frame
        self.lb_frame = tk.Frame(self.root)
        self.lb_frame.pack(fill="both", expand=True)

        # Listbox
        self.lb_tasks = tk.Listbox(self.lb_frame, width=80, height=15, font=('Arial', 14), selectbackground='#007bff',
                                   selectforeground='white')
        self.lb_tasks.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        self.lb_tasks.bind('<Double-Button-1>', self.on_double_click)  # Bind double click to on_double_click method

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.lb_frame, orient='vertical', command=self.lb_tasks.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.lb_tasks.config(yscrollcommand=self.scrollbar.set)

        # Buttons frame
        self.btn_frame = tk.Frame(self.root, bg='lightgrey')
        self.btn_frame.pack(fill="x", padx=10, pady=(20, 10))

        # Buttons
        btn_delete = tk.Button(self.btn_frame, text="Ausgewählte löschen", fg='white', bg='#dc3545', font=('Arial', 14),
                               command=self.delete_task)
        btn_delete.pack(side="left", padx=(0, 10))

        btn_delete_all = tk.Button(self.btn_frame, text="Alle löschen", fg='white', bg='#dc3545', font=('Arial', 14),
                                   command=self.delete_all)
        btn_delete_all.pack(side="left")

        btn_open = tk.Button(self.btn_frame, text="Öffnen", fg='white', bg='#007bff', font=('Arial', 14),
                             command=self.open_data_entry_app)
        btn_open.pack(side="left", padx=(10, 0))

        self.update_listbox()

    def on_double_click(self, event):
        selected_task_index = self.lb_tasks.curselection()
        if selected_task_index:
            selected_task = self.lb_tasks.get(selected_task_index)
            print(f"Double-clicked on: {selected_task}")
            self.open_data_entry_app()

    def load_tasks(self):
        try:
            with open("baustellen.txt", "r") as file:
                self.tasks = file.read().splitlines()
        except FileNotFoundError:
            pass

    def save_tasks(self):
        with open("baustellen.txt", "w") as file:
            file.write("\n".join(self.tasks))

    def update_listbox(self):
        self.lb_tasks.delete(0, "end")
        for task in self.tasks:
            self.lb_tasks.insert("end", task)

    def add_task(self, event=None):
        task = self.txt_input.get().strip()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            self.save_tasks()
            self.txt_input.delete(0, 'end')
        else:
            messagebox.showwarning("Warning", "Bitte geben Sie einen gültigen Baustellennamen ein.")

    def delete_task(self):
        selected_index = self.lb_tasks.curselection()
        if selected_index:
            task = self.lb_tasks.get(selected_index)
            confirm = messagebox.askyesno("Bestätigung",
                                          f"Sind Sie sicher, dass Sie die Baustelle '{task}' löschen möchten?")
            if confirm:
                del self.tasks[selected_index[0]]
                self.update_listbox()
                self.save_tasks()

    def delete_all(self):
        confirm = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie alle Baustellen löschen möchten?")
        if confirm:
            self.tasks.clear()
            self.update_listbox()
            self.save_tasks()
            messagebox.showinfo("Info", "Alle Baustellen wurden erfolgreich gelöscht.")

    def open_data_entry_app(self):
        selected_index = self.lb_tasks.curselection()
        if selected_index:
            global selected_baustelle
            selected_baustelle = self.lb_tasks.get(selected_index)
            self.root.withdraw()
            DataEntryApp()

    def open_details(self):
        selected_index = self.lb_tasks.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            details_window = tk.Toplevel(self.root)
            details_window.title(selected_task)
            details_label = tk.Label(details_window, text=f"Details for {selected_task}")
            details_label.pack()


class DataEntryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Entry")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height - 80}+0+0")
        self.root.wm_attributes("-topmost", True)

        self.create_widgets()

    def create_widgets(self):
        # Gasart
        self.projektnummer_label = tk.Label(self.root, text="Projektnummer:", font=("Arial", 14))
        self.projektnummer_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="e")
        self.projektnummer_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.projektnummer_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Projektnummer
        self.gasart_label = tk.Label(self.root, text="Gasart:", font=("Arial", 14))
        self.gasart_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="e")
        self.gasart_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.gasart_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Messplatz
        self.messplatz_label = tk.Label(self.root, text="Messplatz:", font=("Arial", 14))
        self.messplatz_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="e")
        self.messplatz_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.messplatz_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.beschreibung_label = tk.Label(self.root, text="Beschreibung:", font=("Arial", 14))
        self.beschreibung_label.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="ne")
        self.beschreibung_entry = tk.Text(self.root, font=("Arial", 14), width=80, height=10)
        self.beschreibung_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.weiter_button = tk.Button(self.root, text="Weiter", font=("Arial", 14), command=self.save_and_exit)
        self.weiter_button.grid(row=4, columnspan=2, pady=20)

        self.center_widgets()

    def center_widgets(self):
        # Center all widgets
        for widget in self.root.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    def save_and_exit(self):
        global messplatz
        global projektnummer
        global gasart
        global beschreibung
        gasart = self.gasart_entry.get()
        projektnummer = self.projektnummer_entry.get()
        messplatz = self.messplatz_entry.get()
        beschreibung = self.beschreibung_entry.get("1.0", tk.END)

        messagebox.showinfo("Info", "Daten erfolgreich gespeichert!")

        # Close the window
        confirmation = messagebox.askyesno("Bestätigung",
                                           "Stecker mit Sensor verbinden!\nIst der Stecker verbunden?")

        if confirmation:
            # Proceed to open the DataWindow
            confirmation = messagebox.askyesno("Bestätigung",
                                               "Wird das Rohr durchflossen?",
                                               )

            if confirmation:
                # Proceed to open the DataWindow
                self.root.withdraw()  # Hide root window
                self.data_window = tk.Toplevel(self.root)
                DataWindow(self.data_window)
            else:
                messagebox.showinfo("Information",
                                    "Zugriff verweigert! Bitte stellen Sie sicher, dass das Rohr durchflossen wird",
                                    )
        else:
            messagebox.showinfo("Information",
                                "Zugriff verweigert! Bitte stellen Sie sicher, dass die Pins ordnungsgemäß verbunden "
                                "sind",
                                )


class DataWindow:
    def __init__(self, root):
        self.root = root

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height - 80}+0+0")
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", True)
        self.root.title("ModbusRTUClient - Data")
        self.create_widgets()

    def create_widgets(self):
        # Data labels
        self.tau_label = tk.Label(self.root, text="Drucktaupunkt: 0 °C", font=('Arial', 18))
        self.humidity_label = tk.Label(self.root, text="Relative Feuchtigkeit: 0 %rH", font=('Arial', 18))
        self.pressure_label = tk.Label(self.root, text="Druck: 0 bar", font=('Arial', 18))
        self.temperature_label = tk.Label(self.root, text="Temperatur: 0 °C", font=('Arial', 18))
        self.abs_hum_label = tk.Label(self.root, text="Abs. Feuchtigkeit 0 g/m³", font=('Arial', 18))

        self.tau_label.pack(pady=10)
        self.humidity_label.pack(pady=10)
        self.pressure_label.pack(pady=10)
        self.temperature_label.pack(pady=10)
        self.abs_hum_label.pack(pady=10)

        # Read button
        btn_read = tk.Button(self.root, text="Read", font=('Arial', 18), command=self.update_labels)
        btn_read.pack(pady=10)
        btn_dokumentieren = tk.Button(self.root, text="Dokumentieren", font=('Arial', 18), command=self.create_file)
        btn_dokumentieren.pack(pady=10)

    def update_labels(self):
        ports = serial.tools.list_ports.comports()
        com_port = "COM5"
        for port in ports:
            if "USB Serial Port" in port.description:
                com_port = port.device
        self.data = Mc.client(com_port, 19200, 3, 2, 2301, 8, 'd7af')
        abs_humid = (Calc.absolute_humidity(float(str(self.data[1])), float(str(self.data[3]))))  # * 1000 * 24.45) / 31.998
        self.tau_label.config(text="Drucktaupunkt: " + str(self.data[0]) + " °C")
        self.humidity_label.config(text="Relative Feuchtigkeit: " + str(float(self.data[1])) + " %rH")
        self.pressure_label.config(text="Druck: " + str(self.data[2]) + " bar")
        self.temperature_label.config(text="Temperatur: " + str(self.data[3]) + " °C")
        self.abs_hum_label.config(text="Abs. Feuchtigkeit " + "{:.2f}".format(abs_humid) + " g/m³")

        # Schedule the update every 1000 ms
        self.root.after(1000, self.update_labels)

    def create_file(self):
        try:
            abs_humid = (Calc.absolute_humidity(float(str(self.data[1])), float(str(self.data[3]))))  # * 1000 * 24.45) / 31.9988
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            output_filename = selected_baustelle + "_" + messplatz + ".xlsx"
            output_filepath = f"{desktop_path}/{output_filename}"
            workbook = xlsxwriter.Workbook(output_filepath)
            worksheet = workbook.add_worksheet()

            worksheet.set_paper(9)
            worksheet.set_margins(top=0, bottom=0, left=0, right=0)
            img_path = 'Briefbogen Aktuell 2021.png'
            worksheet.set_column("A:F", 15.4)
            worksheet.insert_image('A1', img_path, {'x_scale': 0.8, 'y_scale': 0.8, 'x_offset': 0, 'y_offset': 0})
            '''
            cell_format = workbook.add_format({
                'font_size': 8,
            })
            cell_format1 = workbook.add_format({
                'align': 'center'
            })
            merge_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                # 'border': 1
            })
            # worksheet.set_column("A:G", 11.29)
            '''

            cell_format = workbook.add_format({
                'font_size': 8,
            })
            worksheet.write("B16", "Prüfauftrag: Feuchtemessung")
            worksheet.write("B17", "Projektnummer: " + projektnummer)
            worksheet.write("D16", "Baustelle:" + selected_baustelle)
            worksheet.write("B19", "Sensor: S220")
            worksheet.write("D19", "Gasart: " + gasart)
            worksheet.add_table('B20:E23', {'header_row': False})
            table_values = [
                ["Messgrößen", "Absolute Feuchtigkeit", "Relative Feuchtigkeit", "Taupunkt"],
                ["Einheit", "g/m³", "%rH", "°C Td"],
                ["MP1", "{:.2f}".format(abs_humid), str(self.data[1]), str(self.data[0]), str(self.data[3])]]

            for i in range(0, len(table_values[0])):
                worksheet.write(f"B{i + 20}", table_values[0][i])
                worksheet.write(f"D{i + 20}", table_values[1][i])
                worksheet.write(f"E{i + 20}", table_values[2][i])

            worksheet.write("B25", "MP1: " + messplatz)
            worksheet.write("B26", "Prüfausdruck Nr.: " + str(1))
            worksheet.write("B27", "Beschreibung: " + beschreibung)
            worksheet.write("B50",
                            "Messbereich: -100 ... +20 °C Td   Genauigkeit: ± 1 °C Td (0 ... 20 °C Td); ± 2 °C Td ("
                            "-60 ... 0 °C Td); ± 3 °C (-100 ... -60 °C Td)",
                            cell_format)
            workbook.close()
            messagebox.showinfo("Info", "Daten erfolgreich dokumentiert!\nDokument ist auf dem Desktop gespeichert!")
        except ValueError:
            messagebox.showinfo("Information", "Fehler! Drück die Read Taste vor dem Dokumentieren!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModbusRTUClientApp(root)
    root.mainloop()
