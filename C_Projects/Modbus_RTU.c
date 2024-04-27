#include <stdio.h>
#include <windows.h>
#include <stdint.h>
#include "HexToDec.c"

#define DEVICE "COM5" // Change this to your device path
#define BAUDRATE CBR_19200
#define MODBUS_SLAVE_ADDR 0x02
#define MODBUS_READ_FUNC 0x03
#define MODBUS_START_ADDR 0x08FD
#define MODBUS_NUM_REGS 0x02 // Number of holding registers to read

int main() {
    HANDLE hSerial;
    DCB dcbSerialParams = {0};
    COMMTIMEOUTS timeouts = {0};

    hSerial = CreateFileA(DEVICE, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (hSerial == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Error opening serial port\n");
        return 1;
    }

    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (!GetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "Error getting device state\n");
        CloseHandle(hSerial);
        return 1;
    }

    dcbSerialParams.BaudRate = BAUDRATE;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity = NOPARITY;
    if (!SetCommState(hSerial, &dcbSerialParams)) {
        fprintf(stderr, "Error setting device parameters\n");
        CloseHandle(hSerial);
        return 1;
    }

    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 50;
    timeouts.WriteTotalTimeoutMultiplier = 10;
    if (!SetCommTimeouts(hSerial, &timeouts)) {
        fprintf(stderr, "Error setting timeouts\n");
        CloseHandle(hSerial);
        return 1;
    }

    // Prepare Modbus request
    unsigned char request[8] = {
            MODBUS_SLAVE_ADDR,     // Slave address
            MODBUS_READ_FUNC,      // Function code: Read Holding Registers
            (MODBUS_START_ADDR >> 8) & 0xFF,  // Starting address high byte
            MODBUS_START_ADDR & 0xFF,         // Starting address low byte
            (MODBUS_NUM_REGS >> 8) & 0xFF,     // Number of registers to read high byte
            MODBUS_NUM_REGS & 0xFF,            // Number of registers to read low byte
            0xD5, 0xF9  // CRC (to be calculated)
    };

    // Calculate CRC (just set to 0 for simplicity)
    request[6] = 0x57;
    request[7] = 0xA8;

    DWORD bytes_written;
    if (!WriteFile(hSerial, request, sizeof(request), &bytes_written, NULL)) {
        fprintf(stderr, "Error writing to serial port\n");
        CloseHandle(hSerial);
        return 1;
    }

    // Read response
    unsigned char response[256];//[256]; // Adjust buffer size as needed
    DWORD bytes_read;
    if (!ReadFile(hSerial, response, sizeof(response), &bytes_read, NULL)) {
        fprintf(stderr, "Error reading from serial port\n");
        CloseHandle(hSerial);
        return 1;
    }
    printf("Response received: ");
    //----------------------------------------
    int Hex[] = {response[2]};
    HexToDec(Hex,2);
    //----------------------------------------

    for (DWORD i = 0; i < 8; i++) {
        printf("%02X ", response[i]); // Print each byte in hexadecimal format
    }
    printf("\n");
    // Process response
    // Assuming Modbus RTU response format: [SlaveAddr FuncCode ByteCount Data CRC]
    // You need to parse the response according to the Modbus protocol

    CloseHandle(hSerial);
    return 0;
}