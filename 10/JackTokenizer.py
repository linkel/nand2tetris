import re
from typing import List
import xml.etree.ElementTree as ET
from enum import Enum 

class TokenType(Enum):
    keyword = 'keyword'
    symbol = 'symbol'
    identifier = 'identifier'
    int_const = 'int_const'
    string_const = 'string_const'

symbol_set = { '{', '}', '(', ')', '[', ']', '.', 
    ',', ';', '+', '*', '/', '&', '|', '<', '>', '=', '~'}

keyword_set = {
    'class',
    'constructor',
    'function',
    'method',
    'field',
    'static',
    'var',
    'int',
    'char',
    'boolean',
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return'
}

digits_set = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
}

class JackTokenizer:
    def __init__(self, file_as_string):
        self.file = file_as_string 
        self.token_list: List[str] = self._process_text(file_as_string)
        self.cursor = -1
        self.current_token = ''
        # print(self.token_list)

    def has_more_tokens(self) -> bool:
        """Return True if there are more tokens in this file."""
        if self.cursor >= len(self.token_list) - 1:
            return False
        return True 

    # Four passes, inefficient.
    def _process_text(self, text: str) -> str:
        intermediate_tokens = self._remove_comments(text).split()
        final_tokens: List[str] = []
        for i, token in enumerate(intermediate_tokens):
            s_start = 0
            c_idx = 0
            while c_idx < len(token):
                if token[c_idx] in symbol_set:
                    if token[s_start: c_idx] != '':
                        final_tokens.append(token[s_start: c_idx])
                    if token[c_idx] != '':
                        final_tokens.append(token[c_idx])
                    c_idx += 1
                    s_start = c_idx
                else:
                    c_idx += 1
            if token[s_start: c_idx] != '':
                final_tokens.append(token[s_start:c_idx])
        return final_tokens

    def _remove_comments(self, text: str) -> str:
        rgx_list = ['\/\/.*\n', '\/\*(.|\n)*?\*\/']
        new_text = text
        for rgx_match in rgx_list:
            new_text = re.sub(rgx_match, '', new_text)
            # print(new_text)
        return new_text

    def advance(self):
        self.cursor += 1
        self.current_token = self.token_list[self.cursor]

    def token_type(self):
        """Returns the type of the current token: 
        keyword, symbol, identifier, int_const, string_const
        """
        tok = self.current_token
        if tok in symbol_set:
            return TokenType.symbol
        elif tok in keyword_set:
            return TokenType.keyword
        elif tok[0] == '"':
            return TokenType.string_const # might want to make sure the string doesn't contain " or \n edge case
        elif tok[0] in digits_set:
            return TokenType.int_const
        else:
            return TokenType.identifier

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
        return self.current_token

    def symbol(self):
        """Returns the character which is the current token. 
        Call this when token type is a symbol.
        """
        return self.current_token 

    def identifier(self):
        """Returns the identifier which is the current token.
        Call this when token type is an identifier
        """
        return self.current_token

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
        return self.current_token.replace('"','')
