import sys
import xml.etree.ElementTree as ET

from JackTokenizer import JackTokenizer, TokenType

def read_file_and_build_xml_tokens_only(f, filename):
    data = f.read()
    tokenizer = JackTokenizer(data)
    root = ET.Element("tokens")
    root.text = '\n'
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        tok = tokenizer.current_token
        if tokenizer.token_type() == TokenType.keyword:
            keyword = tokenizer.keyword()
            sub_el = ET.SubElement(root, "keyword")
            sub_el.text = tok
            sub_el.tail = "\n"
        elif tokenizer.token_type() == TokenType.symbol:
            symbol = tokenizer.symbol()
            sub_el = ET.SubElement(root, "symbol")
            sub_el.text = tok
            sub_el.tail = "\n"

        elif tokenizer.token_type() == TokenType.identifier:
            identifier = tokenizer.identifier()
            sub_el = ET.SubElement(root, "identifier")
            sub_el.text = tok
            sub_el.tail = "\n"

        elif tokenizer.token_type() == TokenType.int_const:
            constant = tokenizer.intVal()
            sub_el = ET.SubElement(root, "integerConstant")
            sub_el.text = tok
            sub_el.tail = "\n"

        elif tokenizer.token_type() == TokenType.string_const:
            constant = tokenizer.stringVal()
            sub_el = ET.SubElement(root, "stringConstant")
            sub_el.text = tok
            sub_el.tail = "\n"

        else:
            raise TypeError("Token type does not match any existing.")
    root.tail = '\n'
    
    tree = ET.ElementTree(root)
    tree.write(f'{filename}_token_output.xml')
    

def test_read_for_testing(f, filename):
    data = f.read()
    tokenizer = JackTokenizer(data)
    while tokenizer.has_more_tokens():
        tokenizer.advance()


# JackAnalyzer, the top level driver
# 1. creates JackTokenizer from the input.jack file
# 2. create an output file that will contain the xml
# 3. use CompilationEngine to compile input into the xml
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: JackAnalyzer.py source")
    path = sys.argv[1]
    with open(path) as f:
        read_file_and_build_xml_tokens_only(f, path)
        # test_read_for_testing(f, path)