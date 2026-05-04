# Compiler: Code Generation

Now we want to generate VM code from the source code. In the previous chapter I wrote a tokenizer and syntax analyzer, which helpfully lets me break down the high level source code into its individual tokens while retaining the meaning and what pieces relate to each other. These tokens now can get read and transformed into the VM code. So I have to write some code that will be a code-gen algorithm.

The textbook notes that I will have to transform an infix expression into postfix expressions. It also talks about an OS API that the compiler will have access to.

There are simple techniques for compiling variables, expressions, strings, and statements. However, how do we deal with objects? An object is a memory block which gets referenced by a variable. The reference variable (e.g., object variable or pointer) will have that memory block's base address. There is an area in the RAM called a heap which is a memory pool for representing objects. We carve bits from that for an object and then when we are done with that object we free that block back to the heap. This memory management stuff will get handled by OS functions.

Compile time vs runtime for constructors--the physical addresses of the objects in RAM don't really matter. The source code and VM code don't know where those are, as long as they have a reference to them, and anything in regards to the memory allocation and real location of objects will only happen during run-time execution.

# Symbol Table: How

Copied the CompilationEngine.py, JackAnalyzer.py, and JackTokenizer.py from chapter 10.

The first bit of this says to build the SymbolTable. Whenever an identifier is seen in the src code, currently the syntax analyzer outputs an XML line. Now I will change it to output "name", "category" (field/static/var/arg/class/subroutine), "index" (the index of the identifier if field/static/var/arg), and "usage" (whether it is declared, or whether it is used).

# Symbol Table: Test

`python JackAnalyzer.py Square/SquareGame.jack`

on MacOS:
`python3 JackAnalyzer.py Square/SquareGame.jack`


and see if you manage to populate the name, category, index, usage, for the first part of the Symbol Table.

Wait, when I compile a subroutine and I try to get classes or subroutines, those don't exist yet in the dictionary because they're declared in another file! Am I supposed to hold off on those, or maybe not add them to a dict? Think about this.

Compilation Engine and Symbol Table here in chapter 11 do have coupling! Syntax analysis was independent and the XML could be validated but now I will have to look up stuff in the symbol tables in the engine to determine the right move sometimes. 

# Symbol Table: Output XML Stage 1

Page 354 in the book mentions to output the xml with identifier type, the running index, and whether it is being declared or used. 
I finally fixed some bugs that were somewhat confusing and got the *_output.xml to print. 

I was getting red herringed by 
```
AttributeError: 'str' object has no attribute 'write'
```

which is actually how the xml python writer works, if tries to call a .write and if it fails it's a filename. 

the other stack trace was still opaque:

```
TypeError: cannot serialize None (type NoneType)
```

This was because when I tried to write the XML tree, the add_identifier in symbol table wasn't returning the index. I had forgotten that I expected an index out of it even. So yeah had to give it something otherwise we're writing a None into the xml value for index. 

then finally I also hit:
```
TypeError: cannot serialize 0 (type int)
```
This is because I was writing index which was an int. And needed to cast it. 

# VM Writer
I added in some of the methods for the VM writer but am thinking my code for the symbol table and putting info on the identifiers has a bug, the outputted XML shows index and stuff on letStatement but I think it should be on the identifier variable? 

I saved the class name and the subroutine name, and gathered the number of arguments it takes, but what I am not confident about is the functions vs methods vs constructors, what you're supposed to do for the implicit this and setting it. I can't remember the earlier VM language chapter super well, I have to go back and look at the spec. 

Verify the following:
```
        if self.vm_writer:
            qualified_name = f"{self.current_class_name}.{self.current_subroutine_name}"
            nlocals = self.symbolTable.counters[Category.var]
            self.vm_writer.write_function(qualified_name, nlocals)
            if self.current_subroutine_kind == "method":
                self.vm_writer.write_push(Segment.ARG, 0)
                self.vm_writer.write_pop(Segment.POINTER, 0)

            if self.current_subroutine_kind == "constructor":
                nfields = self.symbolTable.counters[Category.field]
                self.vm_writer.write_push(Segment.CONST, nfields)
                self.vm_writer.write_call("Memory.alloc", 1)
                self.vm_writer.write_pop(Segment.POINTER, 0)
```

And then in the SquareGame_output.xml for the xml tree, it puts the index and stuff in on the letStatement but I think it actually needs to be on the identifier... It might not matter since I am doing the VM writing and that's the real part. But maybe could have more bugs. 

At least I can see I am generating a .vm file now. Down the line it also needs to handle multiple files and JackAnalyzer needs to be able to take a path. 

# VM Writer - re-fixing an xml issue

I did go and fix up the xml identifiers not having usage info. I still see some identifiers without them but it is better than it was where it was being put on the parent element of the identifier. My call sites are all crazy now since I did a jank fix to save the state in that array and pass it in, with the empty array being passed in for the ones that don't need any state to be saved onto the node... eugh. 

