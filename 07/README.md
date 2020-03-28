# Virtual Machine

When you write a program, there generally needs to be a way to get it to the binary machine language so that the computer can read it.
The thing that turns the written program into binary language is the compiler. 

There's a two-tier translation model that is present in some languages like Java and C# where first the program is translated into an intermediate language (Java bytecode, the instruction set of the JVM, and for C# intermediate language, which runs on the CLR, the common language runtime). Then the intermediate language is translated into the machine language. 
This idea is nice because different CPUs have different implementations of how it understands the binary instructions. By having an intermediate language, now you can run the intermediate language on many different platforms via the CPU running a virtual machine emulating a specific computer. 

For personal clarity, it sounds like assembly language to binary is done via the assembler, and that the compiler will probably directly turn the high level language into binary.

## VM Language for the book

The VM language here consists of four types of commands:

1. Arithmetic
2. Memory access
3. Program flow
4. Subroutine calling commands.

This chapter has to do with building a VM translator, which can turn the arithmetic and memory commands into binary.

## The Stack

Stack is super useful for arithmetic. Load into the stack, if you have an add command, pop one, save it, pop the other, and add the two together then put it back in the stack.
Thus high-level arithmetic and boolean operations can be turned into sequences of stack commands (ch 10-11).

## VM Specification

Arithmetic commands perform arithmetic and logical operations on the stack.

Memory access transfers info between stack and the virtual memory segments. 

Program flow controls conditional and unconditional branching operations.

Function calling controls calling subroutines and then returning from them. 

### Program Flow

- label - label declaration
- goto - unconditional branching
- if-goto - conditional branching
- function functionName nLocals - function declaration with number of locals it's got 
- call Function nArgs - call the function with the number of arguments it has
- return - switch control back to the outer scope

# Compiler and VM Translator

So at the top level, the Jack language will have classes with methods. Foo.jack, Bar.jack.
After getting compiled it'll become Foo.vm, Bar.vm. 
After getting translated by the VM Translator, each method in the class will go from YYY class XXX method to YYY.XXX, making
various multiple files. 

# Standard Mapping


