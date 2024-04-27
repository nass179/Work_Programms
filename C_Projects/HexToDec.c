#include "stdio.h"
#include "math.h"
//method for uint 32
//get a method for float and for int32
//need to sign the binary as negative or positive
void HexToDec(const int Hex[],int len){
    int Dec = 0;
    if(len == 2){
        Dec = Hex[0] * 16 + Hex[1];
    }
    if(len == 3){
        Dec = Hex[0]* (int)pow(16,2) + Hex[1]* (int)pow(16,1) + Hex[2]* (int)pow(16,0);
    }
    if(len == 4){
        Dec = Hex[0]* (int)pow(16,3) + Hex[1]* (int)pow(16,2) + Hex[2]* (int)pow(16,1)+ Hex[3];
    }
    int a = (int) pow(16,2);
    int r = 7*16*16+12*16+15;
    printf("%d \n", Dec);
}/*
int main(){
    int A = 10;
    int B = 11;
    int C = 12;
    int D = 13;
    int E = 14;
    int F = 15;
    int Hex[] = {F, F,F, F};
    int len = sizeof(Hex)/ sizeof(Hex[0]);
    HexToDec(Hex, len);

    return 0;
}*/
//0123456789 ABCDEF
//7D1
//7*16^2 + 13*16^1 + 1*16^0