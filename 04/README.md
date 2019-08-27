# Using the Hack Assembly Language

This section had two assignments--writing a multiplication program in assembly and writing a program that would turn the screen fully black when a key was pressed. 

It was very interesting having to think about how I wanted to use the registers and how I wanted to jump from label to label. The multiplication program was pretty easy but the fill program got me stumped for a bit because of how the screen was actually being used. There were 16 bits (1111111111111111) available in each memory location and so each mem location for the screen range of RAM was representing 16 pixels of space on the screen. Hence initially I had just one line colored for each memory location and was wondering why that was. 

I also was forgetting to reset the pointer to the screen's start location after the first loop. 

Good learning experience! 