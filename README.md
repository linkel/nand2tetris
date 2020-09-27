# The Elements of Computing Systems (nand2tetris)
Nand2tetris is a really cool course available completely free on the internet. The first half of the textbook is freely available. It's nuts! I am currently working on project 5 and stunned by the quality of the course materials and how fun it is to work through the assignments. 

It's about starting with a NAND-gate and then building the rest of the logical chips, building an ALU, sequential chips, learning the Hack computer's assembly language, and exploring computer architecture until you've built enough parts to write Tetris and run it on the computer you wrote. 

## Progress

- Nov 2018: Started course end of Nov 2018.
- Dec 2018: Became super stumped by sequential chips in Project 3 and also took a break to focus on career change. 
- Aug 2019: Resumed the course and understood sequential chips much better (data flip flop, register/bits, tick tock)
- Aug 24, 2019: Finished project 4, the intro to Hack assembly language.
- Mar 2020: After a long break due to switching gears to Skiena, I have returned! Got the Memory chip working.
- Mar 19, 2020: The CPU chip is very buggy right now.
    - Note: I can specify bus pins on the out by writing `out[0..14]=thingthatis15wide`. I didn't know (or forgot) I could do it on the left side too.
- Mar 20, 2020: The CPU chip passes the test script! Also, have completed joining the three parts into the Computer chip.
- Mar 23, 2020: I have an assembler program that works for label-free code (tested with the three provided programs).
- Mar 24, 2020: I have completed the assembler. It works for code with labels. Successfully played Pong translated from assembly to binary via the assembler I wrote.
- Mar 31, 2020: Working slowly on chapter 7, the VM. Writing something to convert from an intermediate language into assembly.
    - Qualms: Is it really okay for me to have 6 - 8 assembly instructions per VM command? Feels like unknown territory.
- Apr 3, 2020: Done with Stage I of Chapter 7 project, which is to implement the VM arithmetic and logical commands with the constant push.
- Apr 19, 2020: Took a break since I started my new job. Now resuming work on the memory access, Stage II of the Chapter 7 project.
    - I got the Basic Test to work, but still need to implement popping of the pointer segment as well as the static segment's push and pop. 
- Apr 24, 2020: Completed all the segments for Stage II. Nice! Think that means I can go on to Chapter 8!
- Aug 29, 2020: Refreshing myself on what I did previously, trying to write commands for the function call. 
- Sep 6, 2020: Got the VM Translator working with SimpleFunction. Still need to handle the init stuff, and correct how I am setting up the function label parts. I think I need to store state on what function I'm in. 
- Sep 19, 2020: I think I have the NestedCall working, without the bootstrap code. I have to think about how the bootstrap code works. 
- Sep 27, 2020: Got the FibonacciElement test working after implementing bootstrap code and compiling multiple vm files into asm file. Verified that NestedCall also works with bootstrap code (last time tested without bootstrap) and just fixed up the code around push and pop of static variables to make StaticsTest work! Hurray! Feels good.