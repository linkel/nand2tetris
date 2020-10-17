# Project for Chapter 09

To familiarize myself with the Jack language in prepartaion for writing the compiler and the OS, I'm to write a program in Jack. 

Ended up going with a modification of the existing square game. Now there are other squares on the screen and going over them destroys them, since they don't redraw onto the screen if they don't move. Made squares smaller and the movement 1 pixel instead so it is smoother. 

If I were wanting to spend more time on this, the next step would be to make some collision detection. Could check to see if your square has overlapped with another square, and if it does, then delete the whole overlapped square and increment your square's size. This would have to be constantly checked in the main game loop.

Though if I had a lot of consumables, it does feel like I'd have to loop through all of them checking against the player square? How do real videogames do this? 

Could go simpler and have the squares you can eat be in fixed positions so I would just check for collision between player square and fixed locations. 
