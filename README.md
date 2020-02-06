# PICLogicEmulator

Software which generates a logic simulating program which can then 
be uploaded to the PIC16F1939 microcontroller. The logic circuits 
are custom drawn by the user in logisim, using basic logic circuits
(NOT, AND, OR, NAND, NOR, XOR, XNOR).

Logic inputs have to be labeled RD0 - RD7 (max 8 inputs). 
Logic outputs have to be labeled RB0 - RB7 (max 8 outputs).

Support for custom selection of port bits as input/output isn't
included, but is easy to implement. 

Requires logisim operators to be facing east (left inputs, right
outputs). Modifying the software so it supports rotations is also
easy to add, but isn't included in this version.









