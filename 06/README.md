# Background

Symbolic vs binary machine language. 

Binary codes represent actual machine instructions.
`110111010010` etc. Depending on the logic design and the machine language, the pattern can cause the hardware to do something like "load contents of Memory[7] into register R3". Lots of opcodes, lots of memory addressing modes, different instruction formats exist for modern machine languages. 

We could document these instructions using a syntax like `LOAD R3, 7` instead. This would then require translation from this symbolic notation into the binary code. Symbolic language is called `assembly` and the translator program is an `assembler`. 

The assemblers parse each command into what it is in binary. 

On the assembly level, writing something like LOAD R3, weight could be loading the contents of the weight variable to r3. Here we have used a variable to represent that memory location. 

There can also be special labels for a location in the program and we can then do a `goto` to go to it. So Variables and Labels introduce symbols into assembly. 

Assemblers then are more complicated than just text processing. Translating the symbols into the binary codes is not complicated. But mapping user-defined variable names and symbolic labels is not trivial! 

## Symbol Resolution

Example rules:
Translated code will be stored in the computer's memory starting at address 0. Variables will be allocated to memory locations starting at address 1024. 

Now we build a symbol table. For each new symbol xxx in the source code, we add a line (xxx,n) to the symbol table where n is the memory address associated with the symbol. Now we translate the program into the symbol-less version. 

Things to consider:

1. This variable allocation assumption limits us to 1024 instructions-long programs. 
2. Each source command is not always mappable on one word. Some assembly commands may be multiple machine instructions (if i=101 goto end) and will need several memory locations. You'd then track how many words each command generates and update the instruction memory counter accordingly. 
3. Each variable is represented by a single memory location, which is naive. There are variables of different types which will occupy different memory spaces. short for 16-bit, double for 64-bits, for example. So then the 16-bit will occupy one memory address on a 16-bit machine and a block of 4 addresses for the 64-bit number. Translator's got to take into account the data types and the word width of the target hardware. 

## Assembler Requirements

Following the machine language specification, this assembler must:

1. Parse the symbolic command into its underlying fields.
2. For each field, generate the bits in machine language.
3. Replace symbolic references with numeric addresses for memory locations.
4. Assemble the binary codes into a machine instruction.

# Specification for Hack .asm to .hack (assembly to binary)

Input: text file program.asm. 
Output: text file program.hack. 
You'd run it by typing in the cmdline, `Assembler prog.asm`

Four modules proposal:
1. Parser module to parse input
2. Code module to provide the binary codes of all the mnemonics
3. SymbolTable module that handles symbols
4. Main program.

This is the first in a series of ive projects that build out the hierarchy of translators--assembler, virtual machine, and compiler.

