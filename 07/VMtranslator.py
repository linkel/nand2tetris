import sys
import os


class Parser:
    """Parses a single vm file."""
    def __init__(self, lines):
        self.lines = lines
        self.curr_line = lines[0]
        self.split_line = self.curr_line.split()
        self.idx = 0
        self.c_arithmetic = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}

    def has_more_commands(self):
        """Return True if there are more commands left for this VM file."""
        return self.idx < len(self.lines) - 1

    def advance(self):
        """Step forward to the next line."""
        self.idx += 1
        self.curr_line = self.lines[self.idx]
        self.split_line = self.curr_line.split()

    def command_type(self):
        """Returns one of: C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL"""
        if self.split_line[0] in self.c_arithmetic:
            return "C_ARITHMETIC"
        elif self.split_line[0] == "push":
            return "C_PUSH"
        elif self.split_line[0] == "pop":
            return "C_POP"
        elif self.split_line[0] == "label":
            return "C_LABEL"
        elif self.split_line[0] == "goto":
            return "C_GOTO"
        elif self.split_line[0] == "if-goto":
            return "C_IF"
        elif self.split_line[0] == "function":
            return "C_FUNCTION"
        elif self.split_line[0] == "return":
            return "C_RETURN"
        elif self.split_line[0] == "call":
            return "C_CALL"
        else:
            raise ValueError

    def arg1(self):
        """Returns the first argument of the current command"""
        return self.split_line[1]

    def arg2(self):
        """Returns the second argument of the current command"""
        return self.split_line[2]


class CodeWriter:
    def __init__(self):
        self.file = None

    def set_filename(self, filename: str):
        """Tells CodeWriter that the translation of a new VM file has begun."""
        self.file = open('{}'.format(filename), "w")

    def write_arithmetic(self, command: str):
        """Writes the assembly code that is the translation of the arithmetic command."""
        if command == "add":
            self.file.write('''@SP
                                M=M-1
                                A=M
                                D=M
                                @SP
                                M=M-1
                                A=M
                                D=D+M
                                M=D
                                @SP
                                M=M+1''')
        else:
            return NotImplemented

    def write_pushpop(self, command: str, segment: str, index: int):
        """Writes the assembly code that is the translation of the given command push or pop."""
        if command == "push":
            # do push stuff
            if segment == "constant":
                self.file.write('@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'.format(index))
            elif segment == "local":
                pass
                # Todo: implement the other push segments
        elif command == "C_POP":
            # do pop stuff
            pass
        else:
            raise ValueError

    def close(self):
        """Close the output file."""
        self.file.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: VMtranslator.py source")
    path = sys.argv[1]
    if os.path.isdir(path):
        # do directory stuff (for each .vm file in there, run the parser thing on it)
        pass
    elif os.path.isfile(path) and os.path.splitext(path)[1] == '.vm':
        with open(sys.argv[1]) as f:
            lines = f.readlines()
            lines = [line.partition('//')[0].strip() for line in lines]
            lines = [line for line in lines if line]
            parser = Parser(lines)
