import os
import xml.etree.ElementTree as ET
from JackTokenizer import JackTokenizer, TokenType

statement_keywords = {"let", "do", "if", "while", "return"}


class CompilationEngine:
    def __init__(self, tokenizer: JackTokenizer, outputFilename):
        self.tree = None
        self.node = None
        self.tokenizer = tokenizer
        self.filename = outputFilename

        self.compile_class()

    def _match_specific_or_any_token_of_type(
        self, curr_tok, curr_type: TokenType, tok, any_tok_of_type
    ):
        if any_tok_of_type == curr_type and len(tok) == 0:
            self.tokenizer.advance()
            el = ET.SubElement(self.node, curr_type.value)
            el.text = f" {curr_tok} "
            el.tail = "\n"
            return True
        elif curr_tok == tok:
            self.tokenizer.advance()
            el = ET.SubElement(self.node, curr_type.value)
            el.text = f" {curr_tok} "
            el.tail = "\n"
            return True
        return False

    """If the current token is equal to the input, move the tokenizer along"""

    def _accept(self, tok, any_tok_of_type=None):
        curr_type = self.tokenizer.token_type()
        if curr_type == TokenType.identifier:
            curr_tok = self.tokenizer.identifier()
            return self._match_specific_or_any_token_of_type(
                curr_tok, curr_type, tok, any_tok_of_type
            )
        elif curr_type == TokenType.keyword:
            curr_tok = self.tokenizer.keyword()
            return self._match_specific_or_any_token_of_type(
                curr_tok, curr_type, tok, any_tok_of_type
            )
        elif curr_type == TokenType.symbol:
            curr_tok = self.tokenizer.symbol()
            return self._match_specific_or_any_token_of_type(
                curr_tok, curr_type, tok, any_tok_of_type
            )
        elif curr_type == TokenType.int_const:
            curr_tok = self.tokenizer.intVal()
            return self._match_specific_or_any_token_of_type(
                curr_tok, curr_type, tok, any_tok_of_type
            )
        elif curr_type == TokenType.string_const:
            curr_tok = self.tokenizer.stringVal()
            return self._match_specific_or_any_token_of_type(
                curr_tok, curr_type, tok, any_tok_of_type
            )
        else:
            raise Exception("unknown type found in accept method")

    def _expect(self, tok, any_tok_of_type=None):
        if self._accept(tok, any_tok_of_type):
            return True
        self.tree.write(f"{os.path.splitext(self.filename)[0]}_error.xml")
        raise Exception(
            f"Expected {tok} but received {self.tokenizer.current_token}. Cursor at {self.tokenizer.cursor}."
        )

    def compile_class(self):
        root_node = ET.Element("class")
        root_node.text = "\n"
        self.tree = ET.ElementTree(root_node)
        self.node = root_node
        self.tokenizer.advance()
        self._expect("class")
        self._expect("", TokenType.identifier)
        self._expect("{")
        while self.tokenizer.token_type() == TokenType.keyword and (
            self.tokenizer.keyword() == "static" or self.tokenizer.keyword() == "field"
        ):
            self.compile_class_var_dec()

        while self.tokenizer.token_type() == TokenType.keyword and (
            self.tokenizer.keyword() == "constructor"
            or self.tokenizer.keyword() == "method"
            or self.tokenizer.keyword() == "function"
        ):
            self.compile_subroutine()
        self._expect("}")
        # TODO Close the xml?

    """Compiles a static declaration or a field declaration."""

    def compile_class_var_dec(self):
        el = ET.SubElement(self.node, "classVarDec")
        self.node = el
        if self._accept("static") or self._accept("field"):
            self.compile_type()
            self._expect("", TokenType.identifier)  # varName
            while self._accept(","):
                self._expect("", TokenType.identifier)
            self._expect(";")

    """Compiles a complete method, function, or constructor"""

    def compile_subroutine(self):
        el = ET.SubElement(self.node, "subroutineDec")
        self.node = el
        if (
            self._accept("constructor")
            or self._accept("method")
            or self._accept("function")
        ):
            if not self._accept("void"):
                self.compile_type()
            self._expect("", TokenType.identifier)  # subroutineName
            self._expect("(")
            self.compile_parameter_list()
            self._expect(")")

            # subroutine body
            el = ET.SubElement(self.node, "subroutineBody")
            self.node = el
            self._expect("{")
            while self.tokenizer.token_type() == TokenType.keyword and (
                self.tokenizer.keyword() == "var"
            ):
                self.compile_var_dec()
            self.compile_statements()
            self._expect("}")

    """Compiles a type, I added this contract for my own ease"""

    def compile_type(self, optional=False):
        if not (self._accept("int") or self._accept("char") or self._accept("boolean")):
            if optional:
                self._accept("", True)
            else:
                self._expect("", TokenType.identifier)

    """Compiles a parameter list, not including the enclosing ()"""

    def compile_parameter_list(self):
        el = ET.SubElement(self.node, "parameterList")
        self.node = el
        if self.compile_type(True):  # bool to show it's optional
            self._expect("", TokenType.identifier)
            while self._accept(","):
                self.compile_type()
                self._expect("", TokenType.identifier)
        # else it's an empty param list

    """Compiles a var declaration"""

    def compile_var_dec(self):
        el = ET.SubElement(self.node, "varDec")
        self.node = el
        self._expect("var")
        self.compile_type()
        self._expect("", TokenType.identifier)
        while self._accept(","):
            self._expect("", TokenType.identifier)
        self._expect(";")

    """Compiles a sequence of statements, not including the enclosing ()"""

    def compile_statements(self):
        el = ET.SubElement(self.node, "statements")
        self.node = el
        while self.tokenizer.token_type() == TokenType.keyword:
            if self.tokenizer.keyword() == "do":
                self.compile_do()
            elif self.tokenizer.keyword() == "let":
                self.compile_let()
            elif self.tokenizer.keyword() == "while":
                self.compile_while()
            elif self.tokenizer.keyword() == "if":
                self.compile_if()
            elif self.tokenizer.keyword() == "return":
                self.compile_return

    def compile_subroutine_call(self):
        self._expect("", TokenType.identifier)
        if self._accept("("):  # go straight to expression list route
            self.compile_expression_list()
            self._expect(")")
        else:
            # self._expect("", TokenType.identifier)  # foo.bar then expression list route
            self._expect(".")
            self._expect("", TokenType.identifier)
            self._expect("(")
            self.compile_expression_list()
            self._expect(")")

    def compile_do(self):
        el = ET.SubElement(self.node, "doStatement")
        self.node = el
        self._expect("do")
        self.compile_subroutine_call()

    def compile_let(self):
        el = ET.SubElement(self.node, "letStatement")
        self.node = el
        self._expect("let")
        self._expect("", TokenType.identifier)
        if self._accept("["):
            self.compile_expression()
            self._expect("]")
        self._expect("=")
        self.compile_expression()
        self._expect(";")

    def compile_while(self):
        el = ET.SubElement(self.node, "whileStatement")
        self.node = el
        self._expect("while")
        self._expect("(")
        self.compile_expression()
        self._expect(")")
        self._expect("{")
        self.compile_statements()
        self._expect("}")

    def compile_return(self):
        el = ET.SubElement(self.node, "returnStatement")
        self.node = el
        self._expect("return")
        self.compile_expression()
        self._expect(";")

    def compile_if(self):
        el = ET.SubElement(self.node, "ifStatement")
        self.node = el
        self._expect("if")
        self._expect("(")
        self.compile_expression()
        self._expect(")")
        self._expect("{")
        self.compile_statements()
        self._expect("}")
        if self._accept("else"):
            self._expect("{")
            self.compile_statements()
            self._expect("}")

    def is_op(keyword):
        return keyword in {"+", "-", "*", "/", "&", "|", "<", ">", "="}

    # I think I need a lookahead here according to the textbook.
    def compile_expression(self):
        el = ET.SubElement(self.node, "expression")
        self.node = el
        self.compile_term()
        while self.tokenizer.token_type() == TokenType.keyword and self.is_op(
            self.tokenizer.keyword()
        ):
            if (
                self._accept("+")
                or self._accept("-")
                or self._accept("*")
                or self._accept("/")
                or self._accept("&")
                or self._accept("|")
                or self._accept("<")
                or self._accept(">")
                or self._accept("=")
            ):
                self.compile_term()

    def compile_term(self):
        el = ET.SubElement(self.node, "term")
        self.node = el
        if self.tokenizer.token_type() == TokenType.identifier:
            self.tokenizer.advance()  # look ahead
            # it is a varName [ expression ]
            if (
                self.tokenizer.token_type() == TokenType.symbol
                and self.tokenizer.symbol() == "["
            ):
                self.tokenizer.retreat()
                self._expect("", TokenType.identifier)
                self._expect("[")
                self.compile_expression()
                self._expect("]")
            # it is a subroutineCall
            elif (
                self.tokenizer.token_type() == TokenType.symbol
                and self.tokenizer.symbol() == "("
            ):
                self.tokenizer.retreat()
                self.compile_subroutine_call()
            # also a subroutineCall
            elif (
                self.tokenizer.token_type() == TokenType.symbol
                and self.tokenizer.symbol() == "."
            ):
                self.tokenizer.retreat()
                self.compile_subroutine_call()
            # just a varName
            else:
                self.tokenizer.retreat()
                self._expect("", TokenType.identifier)

        if not (
            self._accept("", TokenType.int_const)
            or self._accept("", TokenType.string_const)
            or self._accept("", TokenType.keyword)
        ):
            # if it's none of the above then it is a unaryOp term
            if not self._accept("-"):
                self._expect("~")

    def compile_expression_list(self):
        el = ET.SubElement(self.node, "expressionList")
        self.node = el
        self.compile_expression()
        while (
            self.tokenizer.token_type() == TokenType.symbol
            and self.tokenizer.symbol() == ","
        ):
            self._expect(",")
            self.compile_expression()

    # TODO: Unused
    def is_keyword_constant(self, token):
        return token in {"true", "false", "null", "this"}

    def write(self) -> ET:
        self.tree.write
        self.tree.write(self.filename)

    def read_file_and_build_xml_tokens_only(self, tokenizer) -> ET:
        root = ET.Element("tokens")
        root.text = "\n"
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            tok = tokenizer.current_token
            if tokenizer.token_type() == TokenType.keyword:
                keyword = tokenizer.keyword()
                sub_el = ET.SubElement(root, "keyword")
                sub_el.text = f" {tok} "
                sub_el.tail = "\n"
            elif tokenizer.token_type() == TokenType.symbol:
                symbol = tokenizer.symbol()
                sub_el = ET.SubElement(root, "symbol")
                sub_el.text = f" {tok} "
                sub_el.tail = "\n"

            elif tokenizer.token_type() == TokenType.identifier:
                identifier = tokenizer.identifier()
                sub_el = ET.SubElement(root, "identifier")
                sub_el.text = f" {tok} "
                sub_el.tail = "\n"

            elif tokenizer.token_type() == TokenType.int_const:
                constant = tokenizer.intVal()
                sub_el = ET.SubElement(root, "integerConstant")
                sub_el.text = f" {tok} "
                sub_el.tail = "\n"

            elif tokenizer.token_type() == TokenType.string_const:
                constant = tokenizer.stringVal()
                sub_el = ET.SubElement(root, "stringConstant")
                sub_el.text = f" {tok} "
                sub_el.tail = "\n"

            else:
                raise TypeError(
                    f"{tokenizer.token_type} does not match any existing token type."
                )
        root.tail = "\n"

        tree = ET.ElementTree(root)
        return tree
