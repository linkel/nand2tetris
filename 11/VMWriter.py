
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
        self.filename = filename
        self.f = open(filename, 'w')

    def write_push(self, segment: Segment, index: int):
        self.f.write(f'push {segment} {index}\n')

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
        self.f.close()