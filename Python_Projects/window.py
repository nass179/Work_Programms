import tkinter as tk
import Modbus_Communication
#from Modbus_Communication import client
window = tk.Tk()
window.title("ModbusRTU Master")
window.geometry("600x600")
label = tk.Label(text = "test")
label.pack()
window.mainloop()
