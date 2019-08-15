# Notes on Project 3a

## Sequential Chips

I had to revisit this to understand what was happening. Through plain imitation of what was in the textbook, I was able to get the Bit chip going, but I didn't really get what was happening. The register and the RAM in part a were fine since the Bit chip was already doing the confusing DFF sequential work, but I neglected implementing the PC chip and took a long break from this course to work on some other topics (and complete my job searching back in January). 

Looking at it again, I understand it a little better. 

For the Bit, you can draw out a truth table of what happens at each combination of values in a and b and having the Mux's sel on or off (loaded or not for the chip), and then draw out what happens at t=t+1 if nothing changes, or if you modify what's coming in or modify the load.

For example,

```
At t=0

back (a), in (b), load (sel), result (which will be the back for t=1)
0         0        0          0
0         0        1          0
0         1        0          0
0         1        1          1

At t=1

If we don't change anything:

back (a), in (b), load (sel), result (which will be the back for t=2)
0         0        0          0
0         0        1          0
0         1        0          0
1         1        1          1

If we set all our loads to false:

back (a), in (b), load (sel), result (which will be the back for t=2)
0         0        0          0
0         0        0          0
0         1        0          0
1         1        0          1

If we set all the loads to true:

back (a), in (b), load (sel), result (which will be the back for t=2)
0         0        1          0
0         0        1          0
0         1        1          1
1         1        1          1
```
