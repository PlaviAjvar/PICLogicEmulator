#include <xc.h>
#pragma config FOSC=HS,WDTE=OFF,PWRTE=OFF,MCLRE=ON,CP=OFF,CPD=OFF,BOREN=OFF,CLKOUTEN=OFF
#pragma config IESO=OFF,FCMEN=OFF,WRT=OFF,VCAPEN=OFF,PLLEN=OFF,STVREN=OFF,LVP=OFF

char NOT(char x) {
    if(x) return 0;
    return 1;
}

char Buffer(char x) {
    return x;
}

char AND(char x, char y) {
    return (x & y);
}

char OR(char x, char y) {
    return (x | y);
}

char NAND(char x, char y) {
    return !AND(x, y);
}

char NOR(char x, char y) {
    return !OR(x, y);
}

char XOR(char x, char y) {
    return (x ^ y);
}

char XNOR(char x, char y) {
    return !XOR(x, y);
}

void logic_function(void) {
	PORTBbits.RB0 = XOR(PORTDbits.RD0,PORTDbits.RD1);
	PORTBbits.RB1 = AND(PORTDbits.RD0,PORTDbits.RD1);
}

void main(void) {
    // Port B declaration
    TRISB = 0x00;
    ANSELB = 0x00;
    LATB = 0x00;

    // Port D declaration
    TRISD = 0xFF;
    ANSELD = 0x00;

    // infinite loop
    while(1) {
        logic_function(); // set port B to value defined by logic
    }
}