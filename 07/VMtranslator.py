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
        return self.split_line[0]

    def arg2(self):
        """Returns the second argument of the current command"""
        return self.split_line[1]

    def arg3(self):
        """Returns the third argument of the current command"""
        return self.split_line[2]


class CodeWriter:
    def __init__(self):
        self.file = None
        self.label_number = 0

    def set_filename(self, filename: str):
        """Tells CodeWriter that the translation of a new VM file has begun."""
        self.file = open('{}'.format(filename), "w")

    def write_arithmetic(self, command: str):
        """Writes the assembly code that is the translation of the arithmetic command."""
        if command == "add":
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M\n'
                            '@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'M=D+M\n'
                            '@SP\n'
                            'M=M+1\n')
        elif command == "sub":
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M\n'
                            '@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'M=M-D\n'
                            '@SP\n'
                            'M=M+1\n')
        elif command == "neg":
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'M=-M\n'
                            '@SP\n'
                            'M=M+1\n')
        elif command == 'eq':
            label_eq = self._generate_label()
            label_neq = self._generate_label()
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M\n'
                            '@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M-D\n'
                            '@{}\n'
                            'D;JEQ\n'
                            '@SP\n'
                            'A=M\n'
                            'M=0\n'
                            '@{}\n'
                            'D;JNE\n'
                            '({})\n'
                            '@SP\n'
                            'A=M\n'
                            'M=-1\n'
                            '({})\n'
                            '@SP\n'
                            'M=M+1\n'.format(label_eq, label_neq, label_eq, label_neq))
        elif command == 'gt':
            label_gt = self._generate_label()
            label_ngt = self._generate_label()
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M\n'
                            '@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M-D\n'
                            '@{}\n'
                            'D;JGT\n'
                            '@SP\n'
                            'A=M\n'
                            'M=0\n'
                            '@{}\n'
                            'D;JLE\n'
                            '({})\n'
                            '@SP\n'
                            'A=M\n'
                            'M=-1\n'
                            '({})\n'
                            '@SP\n'
                            'M=M+1\n'.format(label_gt, label_ngt, label_gt, label_ngt))
        elif command == 'lt':
            label_lt = self._generate_label()
            label_nlt = self._generate_label()
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M\n'
                            '@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M-D\n'
                            '@{}\n'
                            'D;JLT\n'
                            '@SP\n'
                            'A=M\n'
                            'M=0\n'
                            '@{}\n'
                            'D;JGE\n'
                            '({})\n'
                            '@SP\n'
                            'A=M\n'
                            'M=-1\n'
                            '({})\n'
                            '@SP\n'
                            'M=M+1\n'.format(label_lt, label_nlt, label_lt, label_nlt))
        elif command == "and":
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M\n'
                            '@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'M=D&M\n'
                            '@SP\n'
                            'M=M+1\n')
        elif command == "or":
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'D=M\n'
                            '@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'M=D|M\n'
                            '@SP\n'
                            'M=M+1\n')
        elif command == "not":
            self.file.write('@SP\n'
                            'M=M-1\n'
                            'A=M\n'
                            'M=!M\n'
                            '@SP\n'
                            'M=M+1\n')
        else:
            return NotImplemented

    def write_pushpop(self, command: str, segment: str, index: int):
        """Writes the assembly code that is the translation of the given command push or pop."""
        if command == "C_PUSH":  # TODO: Implement push for static segment
            if segment == "constant":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'.format(index))
            elif segment == "argument":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@ARG\n'
                                'A=D+M\n'  # add offset
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'.format(index))
            elif segment == "local":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@LCL\n'
                                'A=D+M\n'  # add offset
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'.format(index))
            elif segment == "this":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@THIS\n'
                                'A=D+M\n'  # add offset
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'.format(index))
            elif segment == "that":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@THAT\n'
                                'A=D+M\n'  # add offset
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'.format(index))
            elif segment == "pointer":
                if index == 0:
                    self.file.write('@THIS\n'
                                    'D=A\n'                              
                                    '@SP\n'
                                    'A=M\n'
                                    'M=D\n'
                                    '@SP\n'
                                    'M=M+1\n')
                elif index == 0:
                    self.file.write('@THAT\n'
                                    'D=A\n'
                                    '@SP\n'
                                    'A=M\n'
                                    'M=D\n'
                                    '@SP\n'
                                    'M=M+1\n')
                else:
                    raise Exception("Index is out of range for pointer segment, only 0 or 1 permitted")

            elif segment == "temp":
                if int(index) < 0 or int(index) > 7:
                    raise Exception("Out of range for temp segment")
                self.file.write('@{}\n'
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'.format(str(int(index) + 5)))

            else:
                raise Exception("Segment not matching any of expected")
                # Todo: implement the other push segments
        elif command == "C_POP":
            # Todo: implement pop for pointer. Is it necessary for static?
            if segment == "argument":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@ARG\n'
                                'D=D+M\n'
                                '@R13\n'  # Save the segment offset address in R13 register
                                'M=D\n'
                                '@SP\n'  # Pop from stack
                                'M=M-1\n'
                                'A=M\n'
                                'D=M\n'
                                '@R13\n'
                                'A=M\n'  # Set address to what was saved in R13
                                'M=D\n'.format(index))
            elif segment == "local":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@LCL\n'
                                'D=D+M\n'
                                '@R13\n'  # Save the segment offset address in R13 register
                                'M=D\n'
                                '@SP\n'  # Pop from stack
                                'M=M-1\n'
                                'A=M\n'
                                'D=M\n'
                                '@R13\n'
                                'A=M\n'  # Set address to what was saved in R13
                                'M=D\n'.format(index))
            elif segment == "this":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@THIS\n'
                                'D=D+M\n'
                                '@R13\n'  # Save the segment offset address in R13 register
                                'M=D\n'
                                '@SP\n'  # Pop from stack
                                'M=M-1\n'
                                'A=M\n'
                                'D=M\n'
                                '@R13\n'
                                'A=M\n'  # Set address to what was saved in R13
                                'M=D\n'.format(index))
            elif segment == "that":
                self.file.write('@{}\n'
                                'D=A\n'
                                '@THAT\n'
                                'D=D+M\n'
                                '@R13\n'  # Save the segment offset address in R13 register
                                'M=D\n'
                                '@SP\n'  # Pop from stack
                                'M=M-1\n'
                                'A=M\n'
                                'D=M\n'
                                '@R13\n'
                                'A=M\n'  # Set address to what was saved in R13
                                'M=D\n'.format(index))
            elif segment == "temp":
                if int(index) < 0 or int(index) > 7:
                    raise Exception("Out of range for temp segment")
                self.file.write('@SP\n'  # Pop from stack
                                'M=M-1\n'
                                'A=M\n'
                                'D=M\n'
                                '@{}\n' # Go to temp segment offset and store within
                                'M=D\n'.format(str(int(index) + 5)))
            else:
                raise Exception("Segment not matching any of expected")
        else:
            raise ValueError

    def close(self):
        """Close the output file."""
        self.file.close()

    def _generate_label(self) -> str:
        label_number = self.label_number
        self.label_number += 1
        return 'label' + str(label_number)


def run(f, filename):
    lines = f.readlines()
    lines = [line.partition('//')[0].strip() for line in lines]
    lines = [line for line in lines if line]
    parser = Parser(lines)
    code_writer = CodeWriter()
    code_writer.set_filename(os.path.splitext(filename)[0] + '.asm')
    while True:
        if parser.command_type() == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif parser.command_type() == 'C_PUSH' or parser.command_type() == 'C_POP':
            code_writer.write_pushpop(parser.command_type(), parser.arg2(), parser.arg3())
        if not parser.has_more_commands():
            break
        parser.advance()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: VMtranslator.py source")
    path = sys.argv[1]
    if os.path.isdir(path):
        for directory, subdirectories, files in os.walk(path):
            for file in files:
                if file.endswith('.vm'):
                    filepath = os.path.join(path, file)
                    with open(filepath) as f:
                        run(f, filepath)

    elif os.path.isfile(path) and os.path.splitext(path)[1] == '.vm':
        with open(path) as f:
            run(f, path)
