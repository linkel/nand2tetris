## High level languages

High level languages let us abstract away the machine execution. 
The low level will manage the calling subroutine, and the called subroutines. 
What the heck does that mean? So if I were writing something like a math equation, each function I use
like power() or sqrt() is a subroutine and somehow all of these as we go along gets executed with the inputs it gets
and all of this gets nicely terminated and returns the flow of control to the next command.

All the assembly stuff I've been is super sequential, and can only just be read and made to jump to different lines. 

If we want a nice high level language to write in, the low level is handling all these details of the subroutines!

- pass params from the caller to the called subroutine
- saving the state of the caller before switching to execute the called subroutine
- allocate space for the local variables of the subroutine
- jump to execute the subroutine
- return values from the subroutine back to the caller
- recycle the memory space occupied by the subroutine
- reinstate that saved state of the caller
- jump to execute code of the caller following the spot where it was left

Look at that! That's a crapload of stuff to track just for my math equation. 

## Program Flow

Like previously mentioned and seen, the default execution of computer programs is linear. Sequential until broken by branching commands. 
Branching logic uses a goto to tell where to go, or to give a label that is an address to jump to. 

Jump if a given boolean condition is true? Where do we get the boolean expression? We get it from the top of the stack, doing a comparison.

You can see that the VM commands label, goto label, and if-goto label will have something to do with this branching. We will express these commands 
using the branching logic of the assembly language. 

## Labeling

Here, the function labels will all be in the format (function_name$label) so that they're unique. 

This means I should save what function scope I'm in since if there's a need to jump to a label there, I need that function name, right?
 
## Other Notes

Seems like all the folders now for function calls in Proj 8 have Sys.vm files that will create a Sys.init function. So in this implementation of the VM translator, I can always
just commit to expecting that it exists given that the bootstrapper code will always call it. Meaning my previous proj 7 stuff won't have Sys.init and that program isn't compatible (unless I
do something with an argument or using it only if it exists).

## Program Flow

Figure 8.5 in the book details what to do when calling a function, declaring a function, and returning from a function. Will try to implement that. It feels like I could use the write pushpop functions I have already written to simplify some of the pushing. For example, for the call f n command listed in the book, it says:

```
push return-address
push LCL
push ARG
push THIS
push THAT
ARG = SP - n - 5
LCL = SP
goto f
(return-address)
```

And it seems like I could use push constant giving it the special address, and use the subtraction I have already written in chapter 7 to do the part that calculates what ARG is now. From a clean code perspective it feels a little janky to use a push constant and give it the label instead--feels like that should be another function, or should leave a comment about the function's overloadedness. Not 100% sure if it works yet though so will play with it. 

## Pointers

Still not 100% instant knowledge for me when it comes to storing, for example, LCL in a temp variable. LCL is a fixed location in memory meant to store the address to the start of local variables. So if I am storing the address to which LCL points to then that's TEMP = LCL? Versus storing the actual memory fixed location of LCL, which would be TEMP = *LCL? I'd probably never be intending to do the latter. Gonna have to double check my call and return function to make sure I'm not conflating these two things in my generated assembly code.

## *ARG = pop()
I don't think I completely understand this step. We're popping off the top of the stack into ARG. 

## Bugs

Noticed that I made a mistake restoring the variables for THAT, THIS, ARG, and LCL. Instead I was just stuffing the literal integers into them because I didn't access the memory stored at the location they're pointing to via the `A=M` then `D=M` stuff. Remember, every time you set A equal to M, you're now changing what M was. A and M change together--don't get confused by overloading of what the equals assignment operator means to you in other code. 

I also was jumping to code line 14 via using R14 literally, instead of getting the content that R14 had stored in its memory and jumping to what the content was. 

Trying to get it to work with NestedCall. Finding lots of problems. 1. R14 stored the address that stored the line number in the ROM to go to. I accidentally set it up to go to the line number that R14 had stored. 2. Subtraction takes a step back in the stack to work with what's there, then after it gets the new value it steps forward. So I have to make sure I step back in the stack if I want to pop that item, otherwise I'm off by one. Lots of off by one problems... 3. My function calls and returns were off. Still are a bit off. Currently debugging.

Actually, I discovered that for #1 in the paragraph above, I shouldn't store the address that contains the line number in R14! I should just store the damn line number in R14 in the first place, because the address that contains the line number is at risk of being overwritten by stuff while the program is running. So instead of fixing it by going to the address that stores the line number at the end of the RETURN code, I should just make sure I store that line number in R14 directly, at the beginning when I finish calculating the *(FRAME - 5) part. 

Sep 27 2020
I wrote up code to compile multiple vm files into one asm file, which my code previously wasn't doing (it was compiling one by one if a directory was specified) and got that working with the bootstrap code. One insidious problem I fixed was that the labels I was generating weren't unique enough if I was doing it by directory--so if I made label01 for a file1 and then label01 for file2 obviously there are problems here with the overlap. Instead I gave the labels the name file1label01 so file2label01 is unique too.

StaticsTest fails, though...Gotta figure this out. 