#include "stdlib.h"
#include "stdio.h"
int main(){
    char hex_string[] = "07D1";
    unsigned int hex_value; // Assuming it's a 32-bit hexadecimal value
    float float_value;

    // Convert hexadecimal string to unsigned int
    sscanf(hex_string, "%X", &hex_value);

    // Cast the unsigned int to a float
    float_value = *((float*)&hex_value);

    printf("Hexadecimal: %s\n", hex_string);
    printf("Floating-point value: %f\n", float_value);
    return 0;
}