#include <stdio.h>
#include <windows.h>
#include <stdint.h>
#include "HexToDec.c"
#include "stdlib.h"

#define DEVICE "COM3" // Change this to your device path
#define BAUDRATE CBR_19200
#define MODBUS_SLAVE_ADDR 0x02
#define MODBUS_READ_FUNC 0x03
#define MODBUS_START_ADDR 0x08FD//0x07D2//0x08FD
#define MODBUS_NUM_REGS 0x08 // Number of holding registers to read

void hexToDec(unsigned char* sortedresponse){
    char bytes[8];
    bytes[1] = sortedresponse[0] & 0xF;
    bytes[0] = sortedresponse[0] >> 4;
    bytes[3] = sortedresponse[1] & 0xF;
    bytes[2] = sortedresponse[1] >> 4;
    bytes[5] = sortedresponse[2] & 0xF;
    bytes[4] = sortedresponse[2] >> 4;
    bytes[7] = sortedresponse[3] & 0xF;
    bytes[6] = sortedresponse[3] >> 4;
    char num1[8];
    for (int i = 0; i < 8; ++i) {
        sprintf(&num1[i],"%X", bytes[i]);
    }
    //for 32bit float
    unsigned int hex_value;
    float float_value;
    sscanf(num1, "%X", &hex_value);
    float_value = *((float*)&hex_value);
    printf("Hexadecimal: %s\n", num1);
    printf("Value: %f ", float_value);
    /*
    for (int i = 0; i < 8; ++i) {
        printf("%c", num1[i]);
    }
    printf("\n");
    int number[8];
    for (int i = 0; i < 8; ++i) {
        if (num1[i] == 'A'){ number[i] = 10;}
        else if (num1[i] == 'B'){ number[i] = 11;}
        else if (num1[i] == 'C'){ number[i] = 12;}
        else if (num1[i] == 'D'){ number[i] = 13;}
        else if (num1[i] == 'E'){ number[i] = 14;}
        else if (num1[i] == 'F'){ number[i] = 15;}
        else if (num1[i] == 0){number[i] = 0;}
        else{
            number[i] = (int)(num1[i] - '0');
        }
    }

    //for 32bit int
    int32_t a = 0b00000000000000000000000000000000;
    a += number[7];
    a += (number[6] << 4);
    a += (number[5] << 8);
    a += (number[4] << 12);
    a += (number[3] << 16);
    a += (number[2] << 20);
    a += (number[1] << 24);
    a += (number[0] << 28);

    for (int i = 0; i < 8; ++i) {
        printf("%X ",number[i]);
    }
    printf("\n");
    printf("%d ", a);*/

}
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
            //0x65,0x75     // reg 2002
            //0x57,0xA8     //reg 2301
            0xD7, 0xAF // reg 2301-2308   8 registers
    };

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
    unsigned char first[] = {response[5],response[6],response[3],response[4]};//Taupunkt
    unsigned char second[] = {response[9],response[10],response[7],response[8]};//Feuchtigkeit
    unsigned char third[] = {response[13],response[14],response[11],response[12]};//Druck
    unsigned char fourth[] = {response[17],response[18],response[15],response[16]};//Temperatur
    char degree=248;
    printf("Response received: ");
    for (DWORD i = 0; i < 18; i++) {
        printf("%02X ", response[i]); // Print each byte in hexadecimal format
    }
    printf("\n");
    printf("Taupunkt:\n");
    hexToDec(first);
    printf("%cC Td \n",degree);
    printf("Luftfeuchtigkeit:\n");
    hexToDec(second);
    printf("%%rH \n");
    printf("Druck:\n");
    hexToDec(third);
    printf("bar \n");
    printf("Temperatur:\n");
    hexToDec(fourth);
    printf("%cC \n", degree);


    // Process response
    // Assuming Modbus RTU response format: [SlaveAddr FuncCode ByteCount Data CRC]
    // You need to parse the response according to the Modbus protocol

    CloseHandle(hSerial);
    return 0;
}
