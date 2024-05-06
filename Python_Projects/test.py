import tkinter as tk
import tkinter.messagebox as msg

class Baustellenauswahl(tk.Tk):
    def __init__(self, baustellen=None):
        super().__init__()

        if not baustellen:
            self.baustellen = []
        else:
            self.baustellen = baustellen

        self.baustellen_canvas = tk.Canvas(self)
        self.baustellen_frame = tk.Frame(self.baustellen_canvas)
        self.text_frame = tk.Frame(self)

        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.baustellen_canvas.yview)
        self.baustellen_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title("Baustellenauswahl")
        self.geometry("500x500")

        self.baustelle_create = tk.Text(self.text_frame, height=3, bg="white", fg="black")

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.baustellen_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_frame = self.baustellen_canvas.create_window((0, 0), window=self.baustellen_frame, anchor="nw")

        self.baustelle_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.baustelle_create.focus_set()

        self.colour_scheme = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

        self.create_widgets()

    def create_widgets(self):
        auswahl1 = tk.Label(self.baustellen_frame, text="--- Baustelle Hinzufügen ---", bg="lightgrey", fg="black", pady=10)
        auswahl1.bind("<Button-1>", self.remove_baustelle)
        auswahl1.grid(row=0, column=0, columnspan=2, sticky="ew")

        for index, baustelle in enumerate(self.baustellen, start=1):
            baustelle_label = tk.Label(self.baustellen_frame, text=baustelle, pady=10)
            baustelle_label.grid(row=index, column=0, sticky="ew")
            baustelle_delbutton = tk.Button(self.baustellen_frame, text="del", pady=10)
            baustelle_delbutton.grid(row=index, column=1, sticky="ew")

        self.baustellen_frame.grid_columnconfigure(0, weight=1)
        self.baustellen_frame.grid_columnconfigure(1, weight=1)

        self.bind("<Return>", self.add_baustelle)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.baustellen_canvas.bind("<Configure>", self.baustelle_width)

    def add_baustelle(self, event=None):
        baustelle_text = self.baustelle_create.get(1.0, tk.END).strip()

        if len(baustelle_text) > 0:
            self.baustellen.append(baustelle_text)

            baustelle_label = tk.Label(self.baustellen_frame, text=baustelle_text, pady=10)
            baustelle_label.grid(row=len(self.baustellen), column=0, sticky="ew")

            baustelle_delbutton = tk.Button(self.baustellen_frame, text="del", pady=10)
            baustelle_delbutton.grid(row=len(self.baustellen), column=1, sticky="ew")

        self.baustelle_create.delete(1.0, tk.END)

    def remove_baustelle(self, event):
        baustelle_index = int(event.widget.grid_info()["row"])
        if msg.askyesno("Really Delete?", f"Delete {self.baustellen[baustelle_index]}?"):
            del self.baustellen[baustelle_index]
            self.recreate_widgets()

    def recreate_widgets(self):
        for widget in self.baustellen_frame.winfo_children():
            widget.destroy()
        self.create_widgets()

    def on_frame_configure(self, event=None):
        self.baustellen_canvas.configure(scrollregion=self.baustellen_canvas.bbox("all"))

    def baustelle_width(self, event):
        canvas_width = event.width
        self.baustellen_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def mouse_scroll(self, event):
        if event.delta:
            self.baustellen_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.baustellen_canvas.yview_scroll(move, "units")

if __name__ == "__main__":
    baustellenauswahl = Baustellenauswahl()
    baustellenauswahl.mainloop()
