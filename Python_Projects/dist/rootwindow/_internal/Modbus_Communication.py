import serial
import time
import struct


def client(com_port, baudrate, functioncode, slave_id, starting_register, num_of_regs, crc):
    hex_start = hex(starting_register)
    hex_regs_num = hex(num_of_regs)
    hex_data = '0' + str(slave_id) + '0' + str(functioncode) + '0' + hex_start[2:5] + '000' + hex_regs_num[2:3] + crc
    print(hex_data)

    try:
        ser = serial.Serial(com_port, baudrate)
        if ser.is_open:
            print(f"Connected to {com_port} at {baudrate} baud.")
            # Read data from the serial port
            while True:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    # print("Received:", data[0], data[1] , data.hex()[0:6], data.hex()[6:14])
                    # data_add = data.hex()[10:14]+data.hex()[6:10]
                    byte_data1 = bytes.fromhex(data.hex()[6:14])
                    sorted_byte_data = byte_data1[2:] + byte_data1[:2]
                    dewpoint = struct.unpack('>f', sorted_byte_data)
                    formatted_dewpoint = "{:.2f}".format(dewpoint[0])

                    byte_data2 = bytes.fromhex(data.hex()[14:22])
                    sorted_byte_data1 = byte_data2[2:] + byte_data2[:2]
                    rel_humidity = struct.unpack('>f', sorted_byte_data1)
                    formatted_rel_humidity = "{:.2f}".format(rel_humidity[0])

                    byte_data3 = bytes.fromhex(data.hex()[22:30])
                    sorted_byte_data2 = byte_data3[2:] + byte_data3[:2]
                    pressure = struct.unpack('>f', sorted_byte_data2)
                    formatted_pressure = "{:.2f}".format(pressure[0])

                    byte_data4 = bytes.fromhex(data.hex()[30:38])
                    sorted_byte_data3 = byte_data4[2:] + byte_data4[:2]
                    temperature = struct.unpack('>f', sorted_byte_data3)
                    formatted_temperature = "{:.2f}".format(temperature[0])

                    print(dewpoint)
                    print(rel_humidity)
                    print(pressure)
                    print(temperature)

                    data = [formatted_dewpoint, formatted_rel_humidity, formatted_pressure, formatted_temperature]
                    return data

                request = bytes.fromhex(hex_data)
                ser.write(request)
                time.sleep(0.1)

    except serial.SerialException as e:
        print("Error:", e)

    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")


'''data = client('COM6', 19200, 3, 2, 2301, 8, 'd7af')
print(data[0:4])
print("aaa")
'''