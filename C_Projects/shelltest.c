#include <stdio.h>
#include <windows.h>
#include <stdint.h>

int main() {
    int A = 10;
    int D = 13;
    int F = 15;
    int Hex[] = {0,8,F,D};//hex 07D1 in dec  = 2001  2byte 16bit
    int16_t a = 0b0000000000000000;
    a += Hex[3];
    a += (Hex[2] << 4);
    a += (Hex[1] << 8);
    a += (Hex[0] << 12);





    printf("%d",a);
    return 0;
}