## Tokenizer

Run by using `python JackAnalyzer.py Square/SquareGame.jack` from within this folder.

## Notes

4/25/2023
Look at how time flies! Took me 2 years to get around to progressing this. My goodness. 
It successfully runs through the SquareGame.jack file. My first recursive descent LL(1) syntax analyzer! And I basically wrote it all myself, with the exception of looking at the Wikipedia article. Didn't Google, didn't look at Stack Overflow, didn't look at Github, didn't ask ChatGPT anything. That said, I have been writing a grammar for an LR parser at work, so in these long 2 years I've actually put some work into parser-adjacent stuff. 

Well, I say this with lots of excitement, but I still need to check it against a few more files and also consider improving the indentation so I can easily diff against the provided xml examples. 

4/1/2021

Compiler can be broken into syntax analysis and code generation.

Syntax analysis can be broken into tokenizing and parsing.

There's a set of rules, called a context-free grammar, that describes how to properly analyze the syntax of some code.

Tokenizing is when you group the text file's text into chunks, or tokens, like (, or 'a string' or 324234 or &.

### Ponderances

4/16/2021
I notice that when I break the file (as a string) down into the word chunks, for example:

```
/**
Disposes
this
game.
*/

method
void
dispose()
{

do
square.dispose();

do
Memory.deAlloc(this);

return;

}
```

I can see in the above I have to deal with comments.

```
method
void
moveSquare()
{

if
(direction
=
1)
```

And in this snippet I can see that there are sometimes parentheses next to some words, and I will have to peel off the parentheses from the identifier.

4/1/2021

I noticed that a line that is a let statement in the Jack language, like `let direction = 0;` gets correctly compiled by the provided compiler in the tools section of the project. I was thinking that what I'd write would expect that there's a whitespace between the identifier and the equals sign, so it'd fail at `let direction=0`... I guess if I were to write something that was robust it should be able to know, oh, when it's no longer letters and numbers or underscores for the identifier, end it and see if the current character is a new token.

Hence why there's two extra folders right now where I was playing around with that.
