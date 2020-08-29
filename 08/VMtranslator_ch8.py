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
        self.filename = None
        self.label_number = 0

    def set_filename(self, filename: str):
        """Tells CodeWriter that the translation of a new VM file has begun."""
        self.file = open('{}'.format(filename), "w")
        self.filename = os.path.basename(filename);

    def write_init(self):
        # Initialize stack pointer (SP) to 256
        self.file.write('@256\n'
                        'D=A\n'
                        '@SP\n'
                        'M=D\n')
        # TODO: Then call sys.init. Need to implement the function calling process before this.
        # Each translated program has one sys.init.

    def write_label(self, function, label):
        """Write a label belonging to parent function 'function'"""
        self.file.write('({}${})\n'.format(function, label))

    def write_goto(self, function, label=None):
        """Write a goto, to either a function, or a label inside a function."""
        if label:
            self.file.write('@{}${}\n'
                            '0;JMP\n'.format(function, label))
        else:
            self.file.write('@{}\n'
                            '0;JMP\n'.format(function))

    def write_if(self, function, label):
        self.file.write('@SP\n'
                        'M=M-1\n'
                        'A=M\n'
                        'D=M\n'
                        '@{}${}\n'
                        'D;JNE'.format(function, label))

    def write_call(self, function, param_count):
        return_address = self._generate_label()
        self.write_pushpop('C_PUSH', 'constant', return_address)
        self.write_pushpop('C_PUSH', 'constant', 'LCL')
        self.write_pushpop('C_PUSH', 'constant', 'ARG')
        self.write_pushpop('C_PUSH', 'constant', 'THIS')
        self.write_pushpop('C_PUSH', 'constant', 'THAT')
        
        # set ARG to SP - n - 5 where n is param_count
        self.write_pushpop('C_PUSH', 'constant', 'SP')
        self.write_pushpop('C_PUSH', 'constant', str(param_count))
        self.write_arithmetic('sub')
        self.write_pushpop('C_PUSH', 'constant', '5')
        self.write_arithmetic('sub')
        self.file.write('@SP\n'
                        'A=M\n'
                        'D=M\n'
                        '@ARG\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M-1\n')
        # reposition LCL (local) to SP (where we are now on stack)
        self.file.write('@SP\n'
                        'D=M\n'
                        '@LCL\n'
                        'M=D\n')
        # TODO: I need to be able to go to the function, as well as the 
        # if the function has any labels inside of it, to go to its function$label? 
        # Doublecheck correctness of this.
        self.write_goto(function)

        self.file.write('{}\n'.format(return_address))
        

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

    def write_pushpop(self, command: str, segment: str, index: str):
        """Writes the assembly code that is the translation of the given command push or pop."""
        if command == "C_PUSH":
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
                if index == '0':
                    self.file.write('@THIS\n'
                                    'D=M\n'                              
                                    '@SP\n'
                                    'A=M\n'
                                    'M=D\n'
                                    '@SP\n'
                                    'M=M+1\n')
                elif index == '1':
                    self.file.write('@THAT\n'
                                    'D=M\n'
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
            elif segment == "static":
                self.file.write('@{}\n'
                                'D=M\n'
                                '@SP\n'
                                'A=M\n'
                                'M=D\n'
                                '@SP\n'
                                'M=M+1\n'.format(self.filename + '.' + index))
            else:
                raise Exception("Segment not matching any of expected")
        elif command == "C_POP":
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
            elif segment == "pointer":
                if index == '0':
                    self.file.write('@SP\n'
                                    'M=M-1\n'                              
                                    'A=M\n'
                                    'D=M\n'
                                    '@THIS\n'
                                    'M=D\n')
                elif index == '1':
                    self.file.write('@SP\n'
                                    'M=M-1\n'                              
                                    'A=M\n'
                                    'D=M\n'
                                    '@THAT\n'
                                    'M=D\n')
                else:
                    print(index)
                    raise Exception("Index is out of range for pointer segment, only 0 or 1 permitted")
            elif segment == "temp":
                if int(index) < 0 or int(index) > 7:
                    raise Exception("Out of range for temp segment")
                self.file.write('@SP\n'  # Pop from stack
                                'M=M-1\n'
                                'A=M\n'
                                'D=M\n'
                                '@{}\n'  # Go to temp segment offset and store within
                                'M=D\n'.format(str(int(index) + 5)))
            elif segment == "static":
                self.file.write('@SP\n'  # Pop from stack
                                'M=M-1\n'
                                'A=M\n'
                                'D=M\n'
                                '@{}\n'  # Go to the static segment offset and store within
                                'M=D\n'.format(self.filename + "." + index))
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
        command_type = parser.command_type()
        if command_type == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif command_type == 'C_PUSH' or command_type == 'C_POP':
            code_writer.write_pushpop(command_type, parser.arg2(), parser.arg3())
        elif command_type == 'C_LABEL':
            return NotImplemented
        elif command_type == 'C_GOTO':
            return NotImplemented
        elif command_type == 'C_IF':
            return NotImplemented
        elif command_type == 'C_FUNCTION':
            return NotImplemented
        elif command_type == 'C_RETURN':
            return NotImplemented
        elif command_type == 'C_CALL':
            return NotImplemented
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
