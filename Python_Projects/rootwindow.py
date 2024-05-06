import tkinter as tk
import time
import Calc
import Modbus_Communication as Mc


def root_window():
    root = tk.Tk()

    root.geometry("800x500")
    root.title("ModbusRTUClient")
    '''
    def opendata():
        data_window()
        root.destroy()
    '''
    button_frame = tk.Frame(root)
    button_frame.columnconfigure(0, weight=100)
    button_frame.columnconfigure(1, weight=0)
    button_frame.columnconfigure(2, weight=0)
    button_frame.columnconfigure(3, weight=0)

    datalabel = tk.Label(root, text="ModbusClient", font=('Arial', 18))
    datalabel.pack()

    btn_data = tk.Button(button_frame, text="Data", font=('Arial', 18), command=data_window)
    btn_data.grid(row=0, column=0, sticky=tk.W + tk.E)

    btn_calculations = tk.Button(button_frame, text="Calculations", font=('Arial', 18))
    btn_calculations.grid(row=1, column=0, sticky=tk.W + tk.E)

    btn_logs = tk.Button(button_frame, text="Logs", font=('Arial', 18))
    btn_logs.grid(row=2, column=0, sticky=tk.W + tk.E)

    btn_settings = tk.Button(button_frame, text="Settings", font=('Arial', 18))
    btn_settings.grid(row=3, column=0, sticky=tk.W + tk.E)

    button_frame.pack(fill="x", padx=30)

    root.mainloop()


def data_window():
    root = tk.Tk()
    root.geometry("800x500")
    root.title("ModbusRTUClient")
    label = tk.Label(root, text="Data", font=('Arial', 20))
    label.pack(padx=20, pady=20)
    button_frame = tk.Frame(root)
    button_frame.columnconfigure(0, weight=100)
    button_frame.columnconfigure(1, weight=0)
    button_frame.columnconfigure(2, weight=0)
    button_frame.columnconfigure(3, weight=0)

    def update_labels():
        data = Mc.client('COM6', 19200, 3, 2, 2301, 8, 'd7af')
        tau_label.config(text="Taupunkt: " + str(data[0]) + " °C")
        humidity_label.config(text="Relative Luftfeuchtigkeit: " + str(float(data[1])) + " %rH")
        pressure_label.config(text="Druck: " + str(data[2]) + " bar")
        temperature_label.config(text="Temperatur: " + str(data[3]) + " °C")
        # abs_humidity_label.config(text=str(Calc.absolute_humidity(float(data[1]), float(data[3]), float(data[2]))) + " %")
    '''
    def return_to_start():
        root_window()
        root.destroy()
    '''
    btn_read = tk.Button(button_frame, text="Read", font=('Arial', 18), command=update_labels)
    btn_read.grid(row=0, column=0, sticky=tk.W + tk.E)
    # btn_back = tk.Button(button_frame, text="back", font=('Arial', 18), command=return_to_start)
    # btn_back.grid(row=0, column=1, sticky=tk.W + tk.E)
    tau_label = tk.Label(root, text="0", font=('Arial', 18))
    humidity_label = tk.Label(root, text="0", font=('Arial', 18))
    pressure_label = tk.Label(root, text="0", font=('Arial', 18))
    temperature_label = tk.Label(root, text="0", font=('Arial', 18))
    # abs_humidity_label = tk.Label(root, text="0", font=('Arial', 18))
    button_frame.pack(fill="x", padx=30)
    tau_label.pack()
    humidity_label.pack()
    pressure_label.pack()
    temperature_label.pack()
    # abs_humidity_label.pack()


root_window()
