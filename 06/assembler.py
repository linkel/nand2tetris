import sys


class Parser:
    def __init__(self, lines: []):
        self.lines = lines
        self.idx = 0
        self.curr_line = lines[0]
        self.ctriple = None

    def has_more_commands(self):
        """Return True if there are more commands left"""
        return self.idx < len(self.lines) - 1

    def advance(self):
        """Reads the next command"""
        self.idx += 1
        self.curr_line = self.lines[self.idx]
        self.ctriple = None

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
            if self.curr_line[i] == "=":
                equal_idx = i
            if self.curr_line[i] == ";":
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


class Code:
    def __init__(self):
        self.dest_map = {'': '000',
                         'M': '001',
                         'D': '010',
                         'A': '100',
                         'MD': '011',
                         'AM': '101',
                         'AD': '110',
                         'AMD': '111'}

        self.comp_map = {'0': '0101010',
                         '1': '0111111',
                         '-1': '0111010',
                         'D': '0001100',
                         'A': '0110000',
                         '!D': '0001101',
                         '!A': '0110001',
                         '-D': '0001111',
                         '-A': '0110011',
                         'D+1': '0011111',
                         'A+1': '0110111',
                         'D-1': '0001110',
                         'A-1': '0110010',
                         'D+A': '0000010',
                         'D-A': '0010011',
                         'A-D': '0000111',
                         'D&A': '0000000',
                         'D|A': '0010101',
                         'M': '1110000',
                         '!M': '1110001',
                         '-M': '1110011',
                         'M+1': '1110111',
                         'M-1': '1110010',
                         'D+M': '1000010',
                         'D-M': '1010011',
                         'M-D': '1000111',
                         'D&M': '1000000',
                         'D|M': '1010101'}

        self.jump_map = {'': '000',
                         'JGT': '001',
                         'JEQ': '010',
                         'JGE': '011',
                         'JLT': '100',
                         'JNE': '101',
                         'JLE': '110',
                         'JMP': '111'}

    def dest(self, s):
        return self.dest_map[s]

    def comp(self, s):
        return self.comp_map[s]

    def jump(self, s):
        return self.jump_map[s]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: assembler.py filename.txt")
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
            lines = [line.partition('//')[0].strip() for line in lines]
            lines = [line for line in lines if line]
            parser = Parser(lines)

        code = Code()
        with open('Prog.hack', 'w') as f:
            while True:
                if parser.command_type() == 'A_COMMAND':
                    bin_val = bin(int(parser.symbol()))
                    value = str(bin_val)[2:]
                    while len(value) < 15:
                        value = '0' + value
                    instruction = '0' + str(value)
                elif parser.command_type() == 'C_COMMAND':
                    instruction = '111' + code.comp_map[parser.comp()] + code.dest_map[parser.dest()] + code.jump_map[
                        parser.jump()]
                if instruction:
                    f.write(instruction + '\n')
                if parser.has_more_commands():
                    parser.advance()
                else:
                    break
