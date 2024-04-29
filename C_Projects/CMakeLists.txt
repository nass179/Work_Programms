cmake_minimum_required(VERSION 3.27)
project(C_Projects C)

set(CMAKE_C_STANDARD 11)

add_executable(C_Projects main.c
        Modbus_RTU.c
        hSerial.h
        test.c
)
