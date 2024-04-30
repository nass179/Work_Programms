import serial
import time
import struct

def client(Com_Port, Baudrate, Functioncode, Slave_ID, Startingregister, NumOfRegs, CRC):
    hex_start = hex(Startingregister)
    hex_Regsnum = hex(NumOfRegs)
    hex_data = '0' + str(Slave_ID) + '0' + str(Functioncode) + '0'  + hex_start[2:5] + '000' + hex_Regsnum[2:3] + CRC
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
                    float = struct.unpack('>f', sorted_byte_data)
                    print(float)
                  
                request = bytes.fromhex(hex_data)
                ser.write(request)
                
                time.sleep(0.1)

    except serial.SerialException as e:
        print("Error:", e)

    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")
            

client('COM5',19200,3,2,2301,8,'d7af')
print("aaa")
