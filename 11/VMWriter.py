
from enum import Enum


class Segment(Enum):
    CONST = "const"
    ARG = "arg"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

class Command(Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"

class VMWriter:
    def __init__(self, filename):
        self.filename = filename
        self.f = open(filename, 'w')

    def write_push(self, segment: Segment, index: int):
        self.f.write(f'push {segment} {index}\n')

    def write_pop(self, segment: Segment, index: int):
        self.f.write(f'pop {segment} {index}\n')

    def write_arithmetic(self, command: Command):
        self.f.write(f'{command}\n')

    def write_label(self, label: str):
        self.f.write(f'label {label}\n')

    def write_goto(self, label: str):
        self.f.write(f'goto {label}\n')

    def write_if(self, label: str):
        self.f.write(f'if-goto {label}\n')

    def write_call(self, name: str, nargs: int):
        self.f.write(f'call {name} {nargs}\n')
    
    def write_function(self, name: str, nlocals: int):
        self.f.write(f'function {name} {nlocals}\n')

    def write_return(self):
        self.f.write(f'return\n')

    def close(self):
        self.f.close()