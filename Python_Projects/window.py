import tkinter as tk

root = tk.Tk()

root.geometry("800x500")
root.title("ModbusRTUClient")

label = tk.Label(root, text = "test", font = ('Arial, 18'))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack(padx=10, pady=10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

btn1 = tk.Button(buttonframe, text="1", font=('Arial', 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

btn1 = tk.Button(buttonframe, text="2", font=('Arial', 18))
btn1.grid(row=0, column=1, sticky=tk.W+tk.E)

btn1 = tk.Button(buttonframe, text="3", font=('Arial', 18))
btn1.grid(row=0, column=2, sticky=tk.W+tk.E)

btn1 = tk.Button(buttonframe, text="4", font=('Arial', 18))
btn1.grid(row=1, column=0, sticky=tk.W+tk.E)

buttonframe.pack(fill="x")
root.mainloop()