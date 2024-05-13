import tkinter as tk
from tkinter import messagebox

class DataEntryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Entry")
        self.root.geometry("1280x720")

        self.create_widgets()

    def create_widgets(self):
        # Gasart
        self.gasart_label = tk.Label(self.root, text="Gasart:", font=("Arial", 14))
        self.gasart_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="e")
        self.gasart_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.gasart_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Projektnummer
        self.projektnummer_label = tk.Label(self.root, text="Projektnummer:", font=("Arial", 14))
        self.projektnummer_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="e")
        self.projektnummer_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.projektnummer_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Beschreibung
        self.beschreibung_label = tk.Label(self.root, text="Beschreibung:", font=("Arial", 14))
        self.beschreibung_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="ne")
        self.beschreibung_entry = tk.Text(self.root, font=("Arial", 14), width=80, height=10)
        self.beschreibung_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Weiter button
        self.weiter_button = tk.Button(self.root, text="Weiter", font=("Arial", 14), command=self.save_and_exit)
        self.weiter_button.grid(row=3, columnspan=2, pady=20)

        # Center all widgets
        self.center_widgets()

    def center_widgets(self):
        # Center all widgets
        for widget in self.root.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    def save_and_exit(self):
        # Get data from entry fields
        gasart = self.gasart_entry.get()
        projektnummer = self.projektnummer_entry.get()
        beschreibung = self.beschreibung_entry.get("1.0", tk.END)

        # Save data to a file
        with open("data.txt", "w") as file:
            file.write(f"Gasart: {gasart}\n")
            file.write(f"Projektnummer: {projektnummer}\n")
            file.write(f"Beschreibung: {beschreibung}")

        # Notify the user
        messagebox.showinfo("Info", "Data saved successfully!")

        # Close the window
        self.root.destroy()

if __name__ == "__main__":
    app = DataEntryApp()
    app.root.mainloop()
