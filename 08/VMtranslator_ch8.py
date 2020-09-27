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
        self.curr_function = None

    def set_filename(self, filename: str):
        """Tells CodeWriter that the translation of a new VM file has begun."""
        self.file = open('{}'.format(filename), 'a+')
        self.filename = os.path.basename(filename)

    def write_init(self):
        # Initialize stack pointer (SP) to 256
        self.file.write('@256\n'
                        'D=A\n'
                        '@SP\n'
                        'M=D\n')
        self.write_call('Sys.init', 0)

    def write_label(self, label):
        """Write a label belonging to parent function 'function'"""
        if not self.curr_function:
            print('No current function!')
            raise RuntimeError
        self.file.write('({}${})\n'.format(self.curr_function, label))

    def write_goto(self, label):
        """Write a goto to a label inside a function."""
        if self.curr_function:
            self.file.write('@{}${}\n'
                '0;JMP\n'.format(self.curr_function, label))
        else:
            self.file.write('@{}\n'
                    '0;JMP\n'.format(label))

    def write_if(self, label):
        self.file.write('@SP\n'
                        'M=M-1\n'
                        'A=M\n'
                        'D=M\n'
                        '@{}${}\n'
                        'D;JNE\n'.format(self.curr_function, label))

    def _push_contents_of_address(self, address):
        self.file.write('@{}\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n'.format(address))

    def write_call(self, function, param_count):
        return_address = self._generate_label()
        self.write_pushpop('C_PUSH', 'constant', return_address)
        self._push_contents_of_address('LCL')
        self._push_contents_of_address('ARG')
        self._push_contents_of_address('THIS')
        self._push_contents_of_address('THAT')

        # set ARG to SP - n - 5 where n is param_count
        self._push_contents_of_address('SP')
        self.write_pushpop('C_PUSH', 'constant', str(param_count))
        self.write_arithmetic('sub')
        self.write_pushpop('C_PUSH', 'constant', '5')
        self.write_arithmetic('sub')
        self.file.write('@SP\n'
                        'M=M-1\n'
                        'A=M\n'
                        'D=M\n'
                        '@ARG\n'
                        'M=D\n')
        # reposition LCL (local) to SP (where we are now on stack)
        self.file.write('@SP\n'
                        'D=M\n'
                        '@LCL\n'
                        'M=D\n')
        # TODO: I need to be able to go to the function, as well as the 
        # if the function has any labels inside of it, to go to its function$label? 
        # Doublecheck correctness of this.
        self.file.write('@{}\n'
                        '0;JMP\n'.format(function))

        self.file.write('({})\n'.format(return_address))

    def write_function(self, function_name, k):
        """Declare a function function_name that has k local variables"""
        self.file.write('({})\n'.format(function_name))
        for i in range(int(k)):
            self.write_pushpop('C_PUSH', 'constant', '0')

    def write_return(self):
        # save LCL in R15, which is 'FRAME' in Fig 8.5
        self.file.write('@LCL\n'
                        'D=M\n'
                        '@R15\n' 
                        'M=D\n')
        # push contents of R15 to stack and increment stack pointer
        self.file.write('@R15\n'
                        'D=M\n'
                        '@SP\n'
                        'A=M\n'
                        'M=D\n'
                        '@SP\n'
                        'M=M+1\n')
        self.write_pushpop('C_PUSH', 'constant', '5')
        self.write_arithmetic('sub')
        # R14 is 'RETURN', set RETURN to *(FRAME-5)
        self.file.write('@SP\n'
                        'M=M-1\n'
                        'A=M\n'
                        'A=M\n'
                        'D=M\n'
                        '@R14\n'
                        'M=D\n')
        # TODO: The following line is for *ARG = pop() - I don't quite understand this. Need to review it.
        # It seems like I need to bring the stack pointer back one before I do the following?
        # I did this earlier so that my code worked for SimpleFunction but I'm suspecting that I needed to move it back
        # earlier here, for the set RETURN to *(FRAME-5) code I added before. I think maybe I now don't need to do it here. 

        # self.file.write('@SP\n'
        #                 'M=M-1\n')
        self.write_pushpop('C_POP', 'argument', '0')
        # Restore SP, THAT, THIS, ARG, LCL for the caller
        self.file.write('@ARG\n'
                        'D=M+1\n'
                        '@SP\n'
                        'M=D\n'
                        '@R15\n'
                        'M=M-1\n'
                        'A=M\n'
                        'D=M\n'
                        '@THAT\n'
                        'M=D\n'
                        '@R15\n'
                        'M=M-1\n'
                        'A=M\n'
                        'D=M\n'
                        '@THIS\n'
                        'M=D\n'
                        '@R15\n'
                        'M=M-1\n'
                        'A=M\n'
                        'D=M\n'
                        '@ARG\n'
                        'M=D\n'
                        '@R15\n'
                        'M=M-1\n'
                        'A=M\n'
                        'D=M\n'
                        '@LCL\n'
                        'M=D\n')
        # Goto the return address previously saved in R14
        # R14 contains the address on the stack which contains the ROM line number to jump back to. 
        self.file.write('@R14\n'
                        'A=M\n'
                        '0;JMP\n')
        
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
                                'M=M+1\n'.format(self.curr_function + '.' + index))
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
                                'M=D\n'.format(self.curr_function + "." + index))
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
        return 'label' + self.curr_function + str(label_number)


def run_file(f, filename):
    lines = f.readlines()
    lines = [line.partition('//')[0].strip() for line in lines]
    lines = [line for line in lines if line]
    parser = Parser(lines)
    code_writer = CodeWriter()
    code_writer.set_filename(os.path.splitext(filename)[0])
    code_writer.curr_function = os.path.splitext(filename)[0]
    code_writer.write_init()
    while True:
        command_type = parser.command_type()
        if command_type == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif command_type == 'C_PUSH' or command_type == 'C_POP':
            code_writer.write_pushpop(command_type, parser.arg2(), parser.arg3())
        elif command_type == 'C_LABEL':
            code_writer.write_label(parser.arg2())
        elif command_type == 'C_GOTO':
            code_writer.write_goto(parser.arg2())
        elif command_type == 'C_IF':
            code_writer.write_if(parser.arg2())
        elif command_type == 'C_FUNCTION':
            code_writer.write_function(parser.arg2(), parser.arg3())
        elif command_type == 'C_RETURN':
            code_writer.write_return()
        elif command_type == 'C_CALL':
            code_writer.write_call(parser.arg2(), parser.arg3())
        if not parser.has_more_commands():
            break
        parser.advance()


def run_directory(f, filename):
    lines = f.readlines()
    lines = [line.partition('//')[0].strip() for line in lines]
    lines = [line for line in lines if line]
    parser = Parser(lines)
    code_writer = CodeWriter()
    # For a directory, we want to set the filename as the directory and the current function as the filename
    code_writer.set_filename(os.path.splitext(filename)[0].split('/')[-2] + '.asm')
    code_writer.curr_function = os.path.splitext(filename)[0].split('/')[-1]
    code_writer.write_init()
    while True:
        command_type = parser.command_type()
        if command_type == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif command_type == 'C_PUSH' or command_type == 'C_POP':
            code_writer.write_pushpop(command_type, parser.arg2(), parser.arg3())
        elif command_type == 'C_LABEL':
            code_writer.write_label(parser.arg2())
        elif command_type == 'C_GOTO':
            code_writer.write_goto(parser.arg2())
        elif command_type == 'C_IF':
            code_writer.write_if(parser.arg2())
        elif command_type == 'C_FUNCTION':
            code_writer.write_function(parser.arg2(), parser.arg3())
        elif command_type == 'C_RETURN':
            code_writer.write_return()
        elif command_type == 'C_CALL':
            code_writer.write_call(parser.arg2(), parser.arg3())
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
                        run_directory(f, filepath)

    elif os.path.isfile(path) and os.path.splitext(path)[1] == '.vm':
        with open(path) as f:
            run_file(f, path)
