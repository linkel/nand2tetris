// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(START)
    @SCREEN // screen start
    D=A
    @R1 // store current screen location in R1
    M=D
    @24575 // screen end
    D=A
    @R2 // store screen end in R2
    M=D
    @KBD // 24576 keyboard location
    D=M
    @WHITE 
    D;JEQ
    @BLACK
    D;JNE

(WHITE)
    @R0 // store white in R0
    M=0
    @PAINTLOOP
    0;JMP

(BLACK)
    @R0 // store black in R0
    M=-1
    @PAINTLOOP
    0;JMP

(PAINTLOOP)
    @R0 // color stored in R0
    D=M
    @R1 // value is current screen location
    A=M
    M=D // set screen pixel to color
    // if current screen loc - end screen is 0 then jump out
    D=A
    @R2
    D=M-D
    @WHERENEXT
    D;JEQ
    @R1
    D=M+1
    @R1
    M=D
    @PAINTLOOP
    0;JMP

(WHERENEXT)
    @24575
    D=A
    @R1
    D=M-D
    @START
    D;JEQ
    @KBD // repeat to figure out where to go
    D=M
    @WHITE 
    D;JEQ
    @BLACK
    D;JNE