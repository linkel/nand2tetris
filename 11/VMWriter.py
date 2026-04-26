
from enum import Enum


class Segment(Enum):
    CONST = "CONST"
    ARG = "ARG"
    LOCAL = "LOCAL"
    STATIC = "STATIC"
    THIS = "THIS"
    THAT = "THAT"
    POINTER = "POINTER"
    TEMP = "TEMP"

class Command(Enum):
    ADD = "ADD"
    SUB = "SUB"
    NEG = "NEG"
    EQ = "EQ"
    GT = "GT"
    LT = "LT"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

class VMWriter:
    def __init__(self, filename):
        with open(filename, 'w') as f:
            pass 

    def write_push(self, segment: Segment, index: int):
        pass

    def write_pop(self, segment: Segment, index: int):
        pass

    def write_arithmetic(self, command: Command):
        pass

    def write_label(self, label: str):
        pass

    def write_goto(self, label: str):
        pass

    def write_if(self, label: str):
        pass

    def write_call(self, name: str, nargs: int):
        pass
    
    def write_function(self, name: str, nlocals: int):
        pass

    def write_return(self):
        pass 

    def close(self):
        # not sure I need this if I just keep appending to the file with 'x' 
        pass