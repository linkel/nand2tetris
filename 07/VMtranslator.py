import sys


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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: VMtranslator.py source")
