#include <stdio.h>
#include <windows.h>
#include <stdint.h>
#include "stdlib.h"

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



    printf("%d \n",a);
    unsigned char byte = 0x6F;
    char f = byte & 0xF;
    char six = byte >> 4;
    char c[1];
    sprintf(c,"%X",f);
    printf("%c",c[0]);
    /*
    char hexstring[2];
    sprintf(hexstring,"%02X",byte);
    int num[2];
    for (int i = 0; i < 2; ++i) {
        if (hexstring[i] == 'A'){
            num[i] = 10;
        }
        else{
            num[i] = hexstring[i] - '0';
        }

    }
    printf("%c \n", hexstring[0]);
    printf("%d", num[0]);*/
    return 0;
}