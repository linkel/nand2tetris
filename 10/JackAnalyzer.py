import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

# JackAnalyzer, the top level driver
# 1. creates JackTokenizer from the input.jack file
# 2. create an output file that will contain the xml (technically being done by CompilationEngine here, TODO?)
# 3. use CompilationEngine to compile input into the xml
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: JackAnalyzer.py source")
    path = sys.argv[1]
    with open(path) as f:
        data = f.read()
        tokenizer = JackTokenizer(data)
        # tests correctness of the token generation
        # tree = CompilationEngine(tokenizer, f'{os.path.splitext(path)[0]).read_file_and_build_xml_tokens_only(tokenizer)
        tree = CompilationEngine(
            tokenizer, f"{os.path.splitext(path)[0]}_output.xml"
        ).write()
        # tree.write(f'{os.path.splitext(path)[0]}_token_output.xml')
