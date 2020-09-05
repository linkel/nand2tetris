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