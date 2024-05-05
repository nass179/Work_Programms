import serial
import time
import struct

def client(Com_Port, Baudrate, Functioncode, Slave_ID, Startingregister, NumOfRegs, CRC):
    hex_start = hex(Startingregister)
    hex_regs_num = hex(NumOfRegs)
    hex_data = '0' + str(Slave_ID) + '0' + str(Functioncode) + '0' + hex_start[2:5] + '000' + hex_regs_num[2:3] + CRC
    print(hex_data)
    
    try:
        ser = serial.Serial(Com_Port, Baudrate)    
        if ser.is_open:
            print(f"Connected to {Com_Port} at {Baudrate} baud.")
            # Read data from the serial port
            while True:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    #print("Received:", data[0], data[1] , data.hex()[0:6], data.hex()[6:14])
                    #dataadd = data.hex()[10:14]+data.hex()[6:10]
                    byte_data1 = bytes.fromhex(data.hex()[6:14])
                    sorted_byte_data = byte_data1[2:] + byte_data1[:2]
                    dewpoint = struct.unpack('>f', sorted_byte_data)
                    formatted_dewpoint = "{:.2f}".format(dewpoint[0])

                    byte_data2 = bytes.fromhex(data.hex()[14:22])
                    sorted_byte_data1 = byte_data2[2:] + byte_data2[:2]
                    RelHumidity = struct.unpack('>f', sorted_byte_data1)
                    formatted_RelHumidity = "{:.2f}".format(RelHumidity[0])

                    byte_data3 = bytes.fromhex(data.hex()[22:30])
                    sorted_byte_data2 = byte_data3[2:] + byte_data3[:2]
                    pressure = struct.unpack('>f', sorted_byte_data2)
                    formatted_pressure = "{:.2f}".format(pressure[0])

                    byte_data4 = bytes.fromhex(data.hex()[30:38])
                    sorted_byte_data3 = byte_data4[2:] + byte_data4[:2]
                    temperature = struct.unpack('>f', sorted_byte_data3)
                    formatted_temperature = "{:.2f}".format(temperature[0])

                    print(dewpoint)
                    print(RelHumidity)
                    print(pressure)
                    print(temperature)

                    Data = [formatted_dewpoint, formatted_RelHumidity, formatted_pressure, formatted_temperature]
                    return Data
                  
                request = bytes.fromhex(hex_data)
                ser.write(request)
                time.sleep(0.1)

    except serial.SerialException as e:
        print("Error:", e)

    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")
            
'''
data = client('COM4',19200,3,2,2301,8,'d7af')
print(data[0:4])
print("aaa")
'''