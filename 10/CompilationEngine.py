import xml.etree.ElementTree as ET
from JackTokenizer import JackTokenizer, TokenType

class CompilationEngine:
    def __init__(self, tokenizer: JackTokenizer, outputFilename):
        self.tree = None
        self.tokenizer = tokenizer
        self.filename = outputFilename

        self.compile_class()
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            token_type = self.tokenizer.token_type()
            if token_type == TokenType.keyword:
                tok = self.tokenizer.keyword()
                if tok == 'class' | tok == 'method' | tok == 'function' | tok == 'constructor':
                    self.compile_class_var_dec()
                    # TODO: No! I actually want to compile_class_var_dec after the bracket {
                    # Look at the grammar and think about it. 

    def compile_class(self):
        root = ET.Element("class")
        root.text = '\n'
        self.tree = root

    '''Compiles a static declaration or a field declaration.'''
    def compile_class_var_dec(self):
        NotImplemented

    '''Compiles a complete method, function, or constructor'''
    def compile_subroutine(self):
        NotImplemented

    '''Compiles a parameter list, not including the enclosing ()'''
    def compile_parameter_list(self):
        NotImplemented

    '''Compiles a var declaration'''
    def compile_var_dec(self):
        NotImplemented

    '''Compiles a sequence of statements, not including the enclosing ()'''
    def compile_statements(self):
        NotImplemented

    def compile_do(self):
        NotImplemented

    def compile_let(self):
        NotImplemented

    def compile_while(self):
        NotImplemented

    def compile_return(self):
        NotImplemented

    def compile_if(self):
        NotImplemented

    def compile_expression(self):
        NotImplemented

    def compile_term(self):
        NotImplemented

    def compile_expression_list(self):
        NotImplemented

    def write(self) -> ET:
        self.tree.write
        self.tree.write(self.filename)


    def read_file_and_build_xml_tokens_only(self, tokenizer) -> ET:
        root = ET.Element("tokens")
        root.text = '\n'
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            tok = tokenizer.current_token
            if tokenizer.token_type() == TokenType.keyword:
                keyword = tokenizer.keyword()
                sub_el = ET.SubElement(root, "keyword")
                sub_el.text = f' {tok} '
                sub_el.tail = "\n"
            elif tokenizer.token_type() == TokenType.symbol:
                symbol = tokenizer.symbol()
                sub_el = ET.SubElement(root, "symbol")
                sub_el.text = f' {tok} '
                sub_el.tail = "\n"

            elif tokenizer.token_type() == TokenType.identifier:
                identifier = tokenizer.identifier()
                sub_el = ET.SubElement(root, "identifier")
                sub_el.text = f' {tok} '
                sub_el.tail = "\n"

            elif tokenizer.token_type() == TokenType.int_const:
                constant = tokenizer.intVal()
                sub_el = ET.SubElement(root, "integerConstant")
                sub_el.text = f' {tok} '
                sub_el.tail = "\n"

            elif tokenizer.token_type() == TokenType.string_const:
                constant = tokenizer.stringVal()
                sub_el = ET.SubElement(root, "stringConstant")
                sub_el.text = f' {tok} '
                sub_el.tail = "\n"

            else:
                raise TypeError(f"{tokenizer.token_type} does not match any existing token type.")
        root.tail = '\n'
        
        tree = ET.ElementTree(root)
        return tree
