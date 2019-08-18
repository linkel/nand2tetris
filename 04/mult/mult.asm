// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// 1st try: Forgot to store result in R2.
// 2nd try: Reused R0 and consequently ended up squaring R0 instead of adding
// 3rd try: Off by one, when I chose to copy R0 into R3 that meant that 
// when multiplying 3x1 for example, would be adding another 3 to the 3 in R3. 
// Needed to init with a 0.

// First part here checks if either value is 0, if so then result will be zero
    @R0
    D=M
    @ZERO
    D;JEQ
    @R1
    D=M
    @ZERO
    D;JEQ
    @0
    D=A
    @R3
    M=D

// The multiplication logic happens here
(LOOP)
    @R1
    D=M
    @END
    D;JEQ
    @R0
    D=M
    @R3
    M=D+M
    @R1
    M=M-1
    @LOOP
    0;JMP

// Two possible end branches. Could probably be optimized, I think I did this pretty naively
(END)
    @R3
    D=M
    @R2
    M=D
    @END
    0;JMP
(ZERO)
    @0
    D=A
    @R2
    M=D
    @ZERO
    0;JMP