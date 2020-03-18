# Notes

## August 25, 2019

Started reading the course material for the intro to the Hack computer architecture. At this point I've written the processing devices (arithmetic logic unit) and the storage devices (RAM from the data flip flop sequential chip stuff). Now I'm going to get to put it together to make a CPU! 

## Stored Programs, Von Neumann Architecture

So there's a really neat concept called "stored program".

Prior to 1930 mechanical computers had their program code embedded in the hardware. But instead of doing that, what if you could load in the program code and store it temporarily in the computer memory? What if you made it...SOFTWARE? 

Now you can use the same fixed hardware platform but load in a program to be temporarily stored and run, allowing your hardware platform to do totally different things depending on what it's loaded with. 

So if we have a CPU that has a memory device that can get data from an input device and send data to an output device, that's actually a Von Neumann machine. It's the conceptual blueprint of all computers today. 

### Memory

Memory is a sequence of addressable registers. Each one has a unique address and it stores a value. The value is some kind of fixed-size word of information. 

There's one area dedicated to storing data (the arrays, variables, objects to do stuff with), and one area dedicated to storing the program instructions. If they're not in the same physical memory unit this is known as Harvard architecture, which is what the Hack computer is set up with. 

To do stuff with a register, you've got to select the register by supplying an address. This lets you access it immediately. The term Random Access Memory is used to note that each randomly selected register can be reached in the same access time, regardless of the memory size and the register's location in it. 

Data Memory, like I said earlier, stores variables, arrays, and objects. When you select a register, the contents of it can be either read or written to. 

Writing to a register will overwrite the previous value. 

Instruction Memory holds the programs that the computer will execute step by step. 

1. CPU fetches instruction from register
2. CPU decodes it
3. CPU executes the instruction
4. CPU figures out which instruction to fetch next. 

### Central Processing Unit

The CPU, in order to execute programs, makes use of three parts:

1. The arithmetic logic unit
2. Registers,
3. Control unit

The ALU can perform actions like adding numbers, computing bitwise ANDS, comparison, and more depending on implementation. 

The registers boost performance by storing intermediate results rather than storing them in a separtae RAM chip. So CPUs usually have 2 to 32 high speed registers that an each hold a word. 

The control unit decodes the instructions. Computer instructions are represented as binary code, usually 16, 32, or 64 bits wide. 

So now with these three pieces together, the CPU operation will 

1. decode the current instruction
2. execute it
3. figure out which to execute next
4. repeat.

This is sometimes called the "fetch-execute cycle."

### Registers

Anything that can store a chunk of bits that represents a value like a variable, instruction, or address is usually referred to as a register. 

In this discussion we are focusing on CPU-resident registers--the registers that sit inside the CPU. If we didn't have those, then any time the CPU needs to do i/o operations, it would have to access the RAM.

In this theoretical situation: 

1. CPU would send an address value from the CPU to the RAM's address input. 
2. The RAM's direct-access logic would use the address to select a specific memory register.
3. Register's contetnts now travel back to the CPU if it was a read op, or another value from the CPU replaces it if it was a write op. 

This uses at least 2 chips, an address bus, and a data bus. 

Now compare that to the ALU. The ALU is super fast and calculating stuff--but now it'd depend on a slow data storage. Now this is called starvation, which is when a processor is denied the resources it needs to complete its work. 

If we had registers in the CPU itself, we'd save ourselves a lot of time! 

When you specify an instruction that includes a memory register, like M[address] = value, we have to supply the address of that memory! Consequently this would use a lot of bits. In our platform, the Hack computer, we have to use 2 machine instructions, 2 clock cycles even for mundane shit like Memory[address] = 0. 

Because there's fewer CPU resident registers, this means that identifying one just uses a couple of bits. So it'd only need one machine instruction. 

So there's Data Registers in the CPU that hold data, and Address Registers that specify the address. 

Values placed in an address register usually selects that meomry register. This the A thing that was inside of the assembly project, or the @100 setting A to 100. 

Lastly, when the CPU executes a program, it must keep track of the address of the instruction that's gotta be fetched and executed next. The address is usually kept in a register called the program counter, or PC. 

### Input and Output

Computers, to interact with stuff outside, need to use I/O devices. We don't pay attention much to the low-level architecture of these devices because the contract of these devices will (hopefully) make them all look the same to our computer. Memory-mapped I/O is when we make that device look like it's just a regular memory segment to the CPU. Now it gets allocated a spot in memory, which is the memory map for that device. For example, on the keyboard that I used last project, the memory map continually reflects the state of the keyboard--when a user was pressing the keyboard, the value representing the key was in the memory map for that duration. For the screen, the screen would continuously reflect what its memory map had--the 1's would blacken the corresponding pixel. 

These get refreshed several times per second so that the user feels the response is instant. So any computer program could access any I/O device by manipulating the registers in those memory area.s 

Standards are what make sure the contracts for what codes do what on a keyboard, or how a device will interact with the computer. 

So you can design a CPU and platform to be independent of the number or nature or make of these I/O devices! You just allocate a new memory map to that device, pay attention to its base address, and now you just have to manipulate registers in that map according to the contract/protocol to interact with it. 

## The Hack CPU

So the Hack platform consists of:

1. CPU
2. Instruction Memory
3. Data Memory
4. Screen
5. Keyboard

The Hack CPU consists of:

1. ALU 
2. Data Register (D)
3. Address Register (A)
4. Program Counter (PC)

These are 16-bit registers. The D stores data values, the A does three different things (store an inputted value to be saved, or points to where to jump next in instruction memory, or points to an address in the data memory to make use of). 

Hack CPU executes instructions in the 16 bit format of "ixxaccccccdddjjj". 

i-bit is the opcode, or operation code, which tells it what the instruction type is. 0 for A-instruction, 1 for C-instruction. 

If it's an A instruction, then the instruction is treated as a 16-bit binary value that's loaded into the A register. If it's a C-instruction, then we use that formatting that I just typed up there, the ixxaccccccdddjjj stuff. Each one of those characters represents a sequence of control bits that tells it what to do. 

The Hack Instruction Memory consists of:
A direct-access read-only memory device, also called ROM. IT's 32K addressable 16-bit registers. I think we get this pre-made...

The Input/Output devices interact with the memory-mapped buffers as mentioned earlier. 

The Data Memory is created by a chip called Memory. This chip is three 16-bit storage devices--a RAM (16K registers), a Screen (8K registers), and a Keyboard (1 register). 

So it's positions 0 to 16383, then 16384 to 24575, then 24576 on the keyboard. 

The topmost chip is a Computer chip that is the CPU, instruction memory, and data memory.

We have to come up with a logic gate architecture that can execute instructions and determine which instruction to be fetched next. We already have the building blocks all created in the previous projects--now we gotta arrange them and connect them correctly. 

## Instruction Decoding

A continuation of the ixxaccccccdddjjj stuff I mentioned earlier. 

The a and c bits code the comp part of the instruction, and the d and j bits code the destination and jump parts of the instruction, and the x is unused for the C-instruction. 

All these fields get routed to different parts simultaneously of the CPU architecture and different chip-parts will take it in and do what they are made to do to execute the instruction. For example, a C instruction's single a-bit determines whether the ALU will operate on the A register input or the M input, and then the six c-bits decide which function the ALU will compute. The d bits determine which registers "accept" ALU output, and the three j bits then branch control. 

## Instruction Fetching

After executing the current instruction, the CPU determines the address of the next one. The Program Counter always stores the address of the next instruction. We have to connect the PC output of the CPU into the address input of the instruction memory. 

By connecting the PC output into the instruction memory's input, the instruction memory will always emit the instruction that needs to be fetched and executed next. The output of the instruction memory gets connected to the instruction input of the CPU, and then we are done with that fetch-execute cycle. 

So for the Hack computer, the current program gets stored in the instruction memory at address 0. If we want to start or restart execution of a program, we would set the PC to 0. So the CPU's reset input goes straight to the reset input of the PC chip. Asserting the bit on the CPU will affect PC to turn PC = 0 and then we'll go to that first instruction. After execution of the first instruction, we want to do the next, so then PC increments. PC++. 

In other cases, we want to jump to an address of an instruction instead of mindlessly always executing the next line. So then we'd want to write a way to set PC = A if we jump. 

Now we can see that there's two things going on for the PC, at least:

1. If jump, PC = A
2. Otherwise PC++

Whether we are jumping or not depends on the j-bits of the instruction and on the ALU's output. 

So the output of the A register must feed into the input of the PC register. The PC chip has a load-bit that enables it to take in a new input value, or else it'll keep hanging on to what it has. So we can assert the load-bit to execute our PC = A instead of default PC++, and now we can figure out the jump boolean part. 

1. j-bits of current instruction specify the jump condition (our JEQ, JLE stuff). 
2. ALU output bits zr and ng, which can determine if the specified condition got satisfied.

The above are all excellent hints as to how to proceed. Hmmmm. 

## Memory 

As mentioned before, the memory chip is a combo of three lower-level chips. 

1. RAM16K
2. Screen
3. Keyboard

Users of the memory chip will see a single address space from 0 to 24576 (which is 0x6000 in hexadecimal). 

So we will have to split up those address inputs right so that we can select 16394 in the memory address and access address 0 in the Screen chip. We did that in chapter 3 to link sections of memory to other sections. 

## Computer

Combining the 

1. CPU
2. Data Memory: RAM16K/Screen/Keyboard
3. Instruction Memory: ROM32K

will allow us to make our computer! 

## General Perspective

General-purpose computers can execute lots of programs. Dedicated computers are usually embedded in devices like cell phones, game consoles, cameras, weapons, factory equipment, consumer electronics, etc. For those specific applications, a single program is burned into the dedicated computer's Random Access Memory, and it'll only execute that. But otherwise these computers all share similar architecture:

1. Stored programs
2. Fetch-decode-execute logic
3. CPU
4. Registers
5. Program Counters

Most general-purpose computers, unlike Hack, use a single address space for storing both data and instructions. The address for the instruction and for the data must e fed into the same destination of the single address input of the shared address space. 

Usually there's two cycle logic that does this.

1. Fetch Cycle: instruction address is fed to the address input of memory, it emits current instruction, and stores in instruction register.
2. Execute Cycle: decode the instruction, then the optional data address that you get from it is fed to the memory's address input, so that the instruction can manipulate the selected memory location. 

The Hack computer separates the instructions and data into two separate parts so the single cycle logic can be done--however, programs cannot be changed dynamically as a result. Not the clearest on what that means...

Our Hack computer here is also simpler--we don't have to worry about connecting to printers, disks, and networks. We also don't have control over brightness levels per pixel or colors in our screen. Most modern computers allow the CPU to send high-level graphics instructions to a graphics card that then controls the screen. So the CPU doesn't have to draw figures and polygons directly. The GPU would do it with its own embedded chip-set that does it better and more efficiently. It can do very many instances of simple and repetitive math, whereas the CPU can focus hard on a few instances of complex action. Something like that. 

More academic/educational/complex courses/efforts about designing computer hardward is focused around better performance. Stuff like memory hierarchies (cache), I/O device access, pipelining, parallelism, instruction prefetching, and other optimization isn't covered in nand2tetris. 

Sounds like there's two main schools of hardware design.

1. Complex Instruction Set Computing (CISC) - get better performance by providing rich and complex instruction sets. 
2. Reduced Instrucion Set Computing (RISC) - use simple instruction sets to promote faster hardware implementation. 

Hack features neither a strong instruction set nor special hardware acceleration techniques. 



