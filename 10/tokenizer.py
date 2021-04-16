
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
    def __init__(self, file_as_string):
        self.file = file_as_string 
        # cursor's going to go char by char
        self.cursor = 0
        self.current_token = NotImplemented
        self.token_type = NotImplemented

    def has_more_tokens(self):
        """Return True if there are more tokens in this file."""
        if self.cursor >= len(self.file):
            return False
        return True 

    def advance(self):
        # get the next token from input and make it the current
        # run a function that figures out how long the next run of chars
        # is that creates a token and then moves the cursor forward 
        # so we don't repeat read any characters
        # and capture that newly grabbed series of chars or char into a token
        # and set self.current_token to that. 
        token = []
        # skip through spaces
        try:
            while self.file[self.cursor] == ' ':
                self.cursor += 1
            while self.file[self.cursor] != ' ':
                token.append(self.file[self.cursor])
                self.cursor += 1
        except IndexError:
            self.cursor = len(self.file) 
        
        token_as_string = ''.join(token)
        print(token_as_string)
        self.current_token = token_as_string

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
def read_file_and_build_xml(f, filename):
    data = f.read()
    tokenizer = JackTokenizer(data)
    while tokenizer.has_more_tokens:
        tokenizer.advance()
        curr_token = tokenizer.current_token
        if tokenizer.token_type() == TokenType.keyword:
            keyword = tokenizer.keyword()
            # do xml stuff into output file 
        elif tokenizer.token_type() == TokenType.symbol:
            symbol = tokenizer.symbol()
            # do xml stuff, print the right ;lgt looking weird html stuff
        elif tokenizer.token_type() == TokenType.identifier:
            identifier = tokenizer.identifier()
            # do xml stuff, identifier is like a variable name 
        elif tokenizer.token_type() == TokenType.int_const:
            constant = tokenizer.intVal()
            # do xml stuff
        elif tokenizer.token_type() == TokenType.string_const:
            constant = tokenizer.stringVal()
            # do xml stuff
        else:
            raise TypeError("Token type does not match any existing.")

def test_read_for_testing(f, filename):
    data = f.read()
    tokenizer = JackTokenizer(data)
    while tokenizer.has_more_tokens():
        tokenizer.advance()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: tokenizer.py source")
    path = sys.argv[1]
    with open(path) as f:
        # read_file_and_build_xml(f, path)
        test_read_for_testing(f, path)