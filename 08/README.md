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