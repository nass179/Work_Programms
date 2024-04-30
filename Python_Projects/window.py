import tkinter as tk
from tkinter import ttk
#import Modbus_Communication
#from Modbus_Communication import client
window = tk.Tk()
window.title("ModbusRTU Master")
window.geometry("600x600")
frm = ttk.Frame(window, padding = 10)
frm.grid()
ttk.Label(frm, text = 'ModbusRtu').grid(column = 0, row = 0)
ttk.Button(frm, text="Quitttt", command=window.destroy).grid(column=0, row=10)
ttk.Button(frm, text="Quit", command=window.destroy).grid(column = 0, row = 1)
#tk.Label(frm, text = "test").grid(column=0, row=0)

window.mainloop()
