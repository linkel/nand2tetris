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


