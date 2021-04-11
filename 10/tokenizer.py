
import sys
from enum import Enum 

class TokenType(Enum):
    keyword = 'keyword'
    symbol = 'symbol'
    identifer = 'identifier'
    int_const = 'int_const'
    string_const = 'string_const'

symbol_set = { '{', '}', '(', ')', '[', ']', '.', 
    ',', ';', '+', '*', '/', '&', '|', '<', '>', '='}


class JackTokenizer:
    def __init__(self, file):
        self.file = file 
        # cursor's going to go char by char
        self.cursor = NotImplemented
        self.current_token = NotImplemented
        self.token_type = NotImplemented

    def has_more_tokens(self):
        """Return True if there are more tokens in this file."""
        return True 

    def advance(self):
        # get the next token from input and make it the current
        # run a function that figures out how long the next run of chars
        # is that creates a token and then moves the cursor forward 
        # so we don't repeat read any characters
        # and capture that newly grabbed series of chars or char into a token
        # and set self.current_token to that. 
        self.current_token = NotImplemented

    def token_type(self):
        """Returns the type of the current token: 
        keyword, symbol, identifier, int_const, string_const
        """
        # I'm picturing that "advance" will figure out what the token is too
        return self.token_type

    def keyword(self):
        """When token type is keyword, call this to 
        return the type of keyword that is the current token:
        class, method, function, constructor, int, boolean, char, void,
        var, static, field, let, do, if, else, while, return,
        true, false, null, this
        """
        # conditionals here to figure out which keyword it is...
        # I think all of these keywords map the same to their string literal.
        # Also, how do I want to handle types? Declare a bunch of variables to
        # strings? 
        return NotImplemented

    def symbol(self):
        """Returns the character which is the current token. 
        Call this when token type is a symbol.
        """
        # conditionals here to determine which symbol it is
        # I think for the xml there might be something funky here?
        # Like for < and >, not certain
        return NotImplemented 

    def identifier(self):
        """Returns the identifier which is the current token.
        Call this when token type is an identifier
        """
        # Likewise, conditionals here to figure out which identifier it is
        return NotImplemented

    def intVal(self):
        """Returns the integer value of the current token.
        Call this when token type is an int_const
        """
        # cast to int(val) here
        # does this work for everything?
        # There's a limit of 0 to 32767 for int_const
        # but that wouldn't be enforced here
        # That'd be enforced when determining the token, right?
        # Like my advance() function above would have an error
        # if it was a negative number or a number bigger than 32767
        return int(self.current_token)

    def stringVal(self):
        """Returns the string value of the current token,
        without the double quotes. Call this when the
        token type is string_const
        """
        # Can I just replace all double quotes with empty? 
        return self.current_token.replace('"','')

# the f is for reading the file data, the filename will be used to 
# save the output in the right place with the right name.
def read_file(f, filename):
    data = f.read()
    print(data) # if i do data[5] it'll get 6th char which is 'i'
    # so I think I can go ahead and step through this to syntax analyze...
    # how to handle "arbitrary number of spaces, newline, and comments" ?

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: tokenizer.py source")
    path = sys.argv[1]
    with open(path) as f:
        read_file(f, path)