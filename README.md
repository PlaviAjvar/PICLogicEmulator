# PICLogicEmulator

Software which generates a logic emulating program which can then 
be uploaded to the PIC16F1939 microcontroller. The logic circuits 
are custom drawn by the user in Logisim, using basic logic circuits
(NOT, AND, OR, NAND, NOR, XOR, XNOR).

Logic inputs have to be labeled RD0 - RD7 (max 8 inputs). 
Logic outputs have to be labeled RB0 - RB7 (max 8 outputs).
Requires logisim operators to be facing west to east (left inputs, 
right outputs).

To use the software:
1. save logic circuit as logic_circuit.circ in the same folder as
the main project
2. run main.py, a file main.c will be generated
3. build and upload the C code to the microcontroller, manually








