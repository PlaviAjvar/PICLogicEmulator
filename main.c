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
	PORTBbits.RB4 = OR(AND(OR(AND(AND(PORTDbits.RD1,PORTDbits.RD4),XOR(PORTDbits.RD2,PORTDbits.RD5)),AND(PORTDbits.RD2,PORTDbits.RD5)),XOR(PORTDbits.RD3,PORTDbits.RD6)),AND(PORTDbits.RD3,PORTDbits.RD6));
	PORTBbits.RB2 = XOR(AND(PORTDbits.RD1,PORTDbits.RD4),XOR(PORTDbits.RD2,PORTDbits.RD5));
	PORTBbits.RB3 = XOR(OR(AND(AND(PORTDbits.RD1,PORTDbits.RD4),XOR(PORTDbits.RD2,PORTDbits.RD5)),AND(PORTDbits.RD2,PORTDbits.RD5)),XOR(PORTDbits.RD3,PORTDbits.RD6));
	PORTBbits.RB1 = XOR(PORTDbits.RD1,PORTDbits.RD4);
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