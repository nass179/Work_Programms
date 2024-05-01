import tkinter as tk
root = tk.Tk()

root.geometry("800x500")
root.title("ModbusRTUClient")

label = tk.Label(root, text = "ModbusClient", font = ('Arial', 20))
label.pack(padx=20, pady=20)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=100)
buttonframe.columnconfigure(1, weight=0)
buttonframe.columnconfigure(2, weight=0)
buttonframe.columnconfigure(3, weight=0)

btnData = tk.Button(buttonframe, text="Data", font=('Arial', 18))
btnData.grid(row=0, column=0, sticky=tk.W+tk.E)

btnCalculations = tk.Button(buttonframe, text="Calculations", font=('Arial', 18))
btnCalculations.grid(row=1, column=0, sticky=tk.W+tk.E)

btnLogs = tk.Button(buttonframe, text="Logs", font=('Arial', 18))
btnLogs.grid(row=2, column=0, sticky=tk.W+tk.E)

btnSettings = tk.Button(buttonframe, text="Settings", font=('Arial', 18))
btnSettings.grid(row=3, column=0, sticky=tk.W+tk.E)

buttonframe.pack(fill = "x", padx=30)

root.mainloop()
