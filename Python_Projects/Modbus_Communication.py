import serial
import time
import struct
# Define the COM port and baud rate
COM_PORT = 'COM3'  # Change this to the appropriate COM port on your system
BAUD_RATE = 19200
def client():
    try:
        # Open the serial port
        ser = serial.Serial(COM_PORT, BAUD_RATE)
        
        # Check if the port is open
        if ser.is_open:
            print(f"Connected to {COM_PORT} at {BAUD_RATE} baud.")

            # Read data from the serial port
            while True:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    #print("Received:", data[0], data[1] , data.hex()[0:6], data.hex()[6:14])
                    dataadd = data.hex()[10:14]+data.hex()[6:10]
                    byte_data1 = bytes.fromhex(data.hex()[6:14])
                    sorted_byte_data = byte_data1[2:] + byte_data1[:2]
                    float = struct.unpack('>f', sorted_byte_data)
                    print(float)
                hex_data = "020308FD0008D7AF"  
                request = bytes.fromhex(hex_data)
                ser.write(request)
                
                time.sleep(0.1)

    except serial.SerialException as e:
        print("Error:", e)

    finally:
        # Close the serial port
        if ser.is_open:
            ser.close()
            print("Serial port closed.")

#client()
print("aaa")
