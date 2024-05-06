import tkinter as tk
import tkinter.messagebox as msg
import os
import sqlite3


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

        self.scrollbar = tk.Scrollbar(self.baustellen_canvas, orient='vertical', command=self.baustellen_canvas.yview)

        self.baustellen_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title("Baustellenauswahl")
        self.geometry("500x500")

        self.baustelle_create = tk.Text(self.text_frame, height=3, bg="white", fg="black")

        self.baustellen_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_frame = self.baustellen_canvas.create_window((0, 0), window=self.baustellen_frame, anchor="n")

        self.baustelle_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.baustelle_create.focus_set()

        auswahl1 = tk.Label(self.baustellen_frame, text="--- Baustelle Hinzufügen ---", bg="lightgrey", fg="black",
                            pady=10)
        auswahl1.bind("<Button-1>", self.remove_baustelle)
        self.baustellen.append(auswahl1)


        for baustelle in self.baustellen:
            baustelle.pack(side=tk.TOP, fill=tk.X)

        self.bind("<Return>", self.add_baustelle)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.baustellen_canvas.bind("<Configure>", self.baustelle_width)

        self.colour_scheme = [{"bg": "lightgrey", "fg": "black"}, {"bg": "grey", "fg": "white"}]

        '''current_baustelle = self.load_baustellen()
        for baustelle in current_baustelle:
            baustelle_text = baustelle[0]
            self.add_baustelle(None, baustelle_text, True)'''

    def add_baustelle(self, event=None, from_db=False):
        baustelle_text = self.baustelle_create.get(1.0, tk.END).strip()
        '''if not baustelle_text:
            new_baustelle = self.baustelle_create.get(1.0, tk.END).strip()'''

        if len(baustelle_text) > 0:
            new_baustelle = tk.Label(self.baustellen_frame, text=baustelle_text, pady=10)
            new_delbutton = tk.Button(self.baustellen_frame, text="del", pady=10)

            self.set_baustelle_colour(len(self.baustellen), new_baustelle)
            # loescht eintrag bi mausklick
            new_baustelle.bind("<Button-1>", self.remove_baustelle)

            new_baustelle.pack(side=tk.TOP, fill=tk.X)
            self.baustellen.append(new_baustelle)

            '''if not from_db:
                self.save_baustelle(baustelle_text)'''

        self.baustelle_create.delete(1.0, tk.END)

    def remove_baustelle(self, event):
        baustelle = event.widget
        if msg.askyesno("Really Delete?", "Delete " + baustelle.cget("text") + "?"):
            self.baustellen.remove(event.widget)

            '''delete_baustelle_query = "DELETE FROM baustellen WHERE baustelle=?"
            delete_baustelle_data = (baustelle.cget("text"))
            self.runQuery(delete_baustelle_query, delete_baustelle_data)'''

            event.widget.destroy()

            self.recolour_baustellen()

    def recolour_baustellen(self):
        for index, baustelle in enumerate(self.baustellen):
            self.set_baustelle_colour(index, baustelle)

    def set_baustelle_colour(self, position, baustelle):
        baustelle_style_choice = divmod(position, 2)

        my_scheme_choice = self.colour_scheme[baustelle_style_choice[1]]

        baustelle.configure(bg=my_scheme_choice["bg"], fg=my_scheme_choice["fg"])

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

    '''def save_baustelle(self, baustelle):
        insert_baustelle_query = "INSERT INTO baustelle VALUES (?)"
        insert_baustelle_data = (baustelle,)
        self.runQuery(insert_baustelle_query, insert_baustelle_data)

    def load_baustellen(self):
        load_baustellen_query = "SELECT baustelle FROM baustelle"
        my_baustellen = self.runQuery(load_baustellen_query, receive=True)
        return my_baustellen

    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect("baustellen.db")
        cursor = conn.cursor()
        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        if receive:
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()

    @staticmethod
    def firstTimeDB():
        create_tables = "CREATE TABLE baustellen (baustelle TEXT)"
        Baustellenauswahl.runQuery(create_tables)

        default_baustelle_query = "INSERT INTO baustelle VALUES (?)"
        default_baustelle_data = ("--- Baustelle Hinzufügen ---",)
        Baustellenauswahl.runQuery(default_baustelle_query, default_baustelle_data)'''


if __name__ == "__main__":
    baustellenauswahl = Baustellenauswahl()
    baustellenauswahl.mainloop()
