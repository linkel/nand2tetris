## Tokenizer

4/1/2021

Compiler can be broken into syntax analysis and code generation. 

Syntax analysis can be broken into tokenizing and parsing. 

There's a set of rules, called a context-free grammar, that describes how to properly analyze the syntax of some code. 

Tokenizing is when you group the text file's text into chunks, or tokens, like (, or 'a string' or 324234 or &. 

### Ponderances

I noticed that a line that is a let statement in the Jack language, like `let direction = 0;` gets correctly compiled by the provided compiler in the tools section of the project. I was thinking that what I'd write would expect that there's a whitespace between the identifier and the equals sign, so it'd fail at `let direction=0`... I guess if I were to write something that was robust it should be able to know, oh, when it's no longer letters and numbers or underscores for the identifier, end it and see if the current character is a new token. 

Hence why there's two extra folders right now where I was playing around with that. 