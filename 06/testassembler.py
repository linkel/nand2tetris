import unittest
from .assembler import Parser


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        test_lines = ['@123','M=1','@456','M=0','D;JGT','D=D-A;JNE']
        self.parser = Parser(test_lines)

    def test_command_type(self):
        self.assertEqual(self.parser.command_type(), 'A_COMMAND')
        self.parser.advance()
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')
        self.parser.advance()
        self.assertEqual(self.parser.command_type(), 'A_COMMAND')
        self.parser.advance()
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')
        self.parser.advance()
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')
        self.parser.advance()
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')




