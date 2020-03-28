import sys

class Parser:
    """Parses a single vm file."""
    def __init__(self, lines):
        self.curr_line = lines[0]

    def has_more_commands(self):
        """Return True if there are more commands left for this VM file."""
        return NotImplemented

    def advance(self):
        """Step forward to the next line."""
        return NotImplemented

    def command_type(self):
        """Returns one of: C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL"""
        return NotImplemented

    def arg1(self):
        """Returns the first argument of the current command"""

    def arg2(self):
        """Returns the second argument of the current command"""
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: VMtranslator.py source")
