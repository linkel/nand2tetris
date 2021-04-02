
import sys

def read_file(f, filename):
    lines = f.readlines()
    print(lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: tokenizer.py source")
    path = sys.argv[1]
    with open(path) as f:
        read_file(f, path)