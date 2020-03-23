import sys


class Parser:
    def __init__(self, lines: []):
        self.lines = lines
        self.idx = 0
        self.curr_line = lines[0]
        self.ctriple = None

    def has_more_commands(self):
        """Return True if there are more commands left"""
        return self.idx < self.lines

    def advance(self):
        """Reads the next command"""
        self.idx += 1
        self.curr_line = self.lines[self.idx]

    def command_type(self):
        """Returns the type of the current command"""
        if self.curr_line[0] == "@":
            return "A_COMMAND"
        elif '=' in self.curr_line or ';' in self.curr_line:
            return "C_COMMAND"
        else:
            return "L_COMMAND"

    def symbol(self):
        """Returns the symbol or decimal of the current command"""
        cmd_type = self.command_type()
        if cmd_type == "A_COMMAND":
            return self.curr_line[1:]
        if cmd_type == "L_COMMAND":
            raise NotImplemented

    def _cinstruction(self):
        if self.command_type() != "C_COMMAND":
            raise Exception("Not a c-instruction")
        equal_idx = None
        semicolon_idx = None
        dest = ''
        comp = ''
        jump = ''
        for i in range(len(self.curr_line)):
            if self.curr_line == "=":
                equal_idx = i
            if self.curr_line == ";":
                semicolon_idx = i
        if equal_idx and semicolon_idx:
            dest = self.curr_line[0:equal_idx]
            comp = self.curr_line[equal_idx + 1: semicolon_idx]
            jump = self.curr_line[semicolon_idx + 1:]
        elif equal_idx and not semicolon_idx:
            dest = self.curr_line[0:equal_idx]
            comp = self.curr_line[equal_idx + 1:]
        elif not equal_idx and semicolon_idx:
            comp = self.curr_line[0:semicolon_idx]
            jump = self.curr_line[semicolon_idx + 1:]
        self.ctriple = (dest, comp, jump)

    def dest(self):
        """Returns the destination mnemonic for the current C-command"""
        if self.ctriple:
            return self.ctriple[0]
        self._cinstruction()
        return self.ctriple[0]

    def comp(self):
        """Returns the comp mnemonic for the current C-command"""
        if self.ctriple:
            return self.ctriple[1]
        self._cinstruction()
        return self.ctriple[1]

    def jump(self):
        """Returns the jump mnemonic for the current C-command"""
        if self.ctriple:
            return self.ctriple[2]
        self._cinstruction()
        return self.ctriple[2]

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("usage: assembler.py filename.txt")
    else:
        with open(sys.argv[0]) as f:
            lines = f.readlines()
            parser = Parser(lines)
