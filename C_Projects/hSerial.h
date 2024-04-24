//
// Created by henry on 22.04.2024.
//

#ifndef C_PROJECTS_HSERIAL_H
#define C_PROJECTS_HSERIAL_H
#define DEVICE "COM5" // Change this to your device path
#define BAUDRATE CBR_19200
#define MODBUS_SLAVE_ADDR 0x02
#define MODBUS_READ_FUNC 0x03
#define MODBUS_START_ADDR 0x7D2
#define MODBUS_NUM_REGS 0x01 // Number of holding registers to read

#endif //C_PROJECTS_HSERIAL_H
