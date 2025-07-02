import re
from typing import List
import xml.etree.ElementTree as ET
from enum import Enum


class TokenType(Enum):
    keyword = "keyword"
    symbol = "symbol"
    identifier = "identifier"
    int_const = "integerConstant"
    string_const = "stringConstant"


class Usage(Enum):
    declared = "declared"
    used = "used"


class Category(Enum):
    field = "field"
    static = "static"
    var = "var"
    arg = "arg"
    aclass = "aclass"
    subroutine = "subroutine"


symbol_set = {
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
}

keyword_set = {
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
}

digits_set = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}


class JackTokenizer:
    def __init__(self, file_as_string):
        self.file = file_as_string
        self.token_list: List[str] = self._process_text(file_as_string)
        self.cursor = -1
        self.current_token = ""
        # print(self.token_list)

    def has_more_tokens(self) -> bool:
        """Return True if there are more tokens in this file."""
        if self.cursor >= len(self.token_list) - 1:
            return False
        return True

    # Four passes, inefficient.
    def _process_text(self, text: str) -> str:
        s = self._remove_comments(text)
        intermediate_tokens = re.findall('(?:".*?"|\S)+', s)
        final_tokens: List[str] = []
        for i, token in enumerate(intermediate_tokens):
            s_start = 0
            c_idx = 0
            # we have already split based on whitespace so now we "split" based on symbols
            while c_idx < len(token):
                if token[c_idx] in symbol_set:
                    if token[s_start:c_idx] != "":
                        final_tokens.append(token[s_start:c_idx])
                    if token[c_idx] != "":
                        final_tokens.append(token[c_idx])
                    c_idx += 1
                    s_start = c_idx
                else:
                    c_idx += 1
            if token[s_start:c_idx] != "":
                final_tokens.append(token[s_start:c_idx])
        return final_tokens

    def _remove_comments(self, text: str) -> str:
        rgx_list = ["\/\/.*\n", "\/\*(.|\n)*?\*\/"]
        new_text = text
        for rgx_match in rgx_list:
            new_text = re.sub(rgx_match, "", new_text)
            # print(new_text)
        return new_text

    def advance(self):
        self.cursor += 1
        if self.cursor < len(self.token_list):
            self.current_token = self.token_list[self.cursor]

    """Can I implement lookahead with this?"""

    def retreat(self):
        self.cursor -= 1
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
            return (
                TokenType.string_const
            )  # might want to make sure the string doesn't contain " or \n edge case
        # also if string constant has spaces inside.
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
        val = int(self.current_token)
        if val > 32767 or val < 0:
            print(f"{val} is out of range of 0 to 32767")
            raise Exception(f"{val} is out of range of 0 to 32767")
        return int(self.current_token)

    def stringVal(self):
        """Returns the string value of the current token,
        without the double quotes. Call this when the
        token type is string_const
        """
        return self.current_token.replace('"', "")
