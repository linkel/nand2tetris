from SymbolTable import SymbolTable
from JackTokenizer import Category
tbl = SymbolTable()

# class SquareGame {
#   field Square square; // the square of this game
#   field int direction; // the square's current direction: 
#                        // 0=none, 1=up, 2=down, 3=left, 4=right

tbl.add_identifier('SquareGame', Category.aclass)
tbl.add_identifier('square', Category.field)
tbl.add_identifier('direction', Category.field)

print(tbl.get_index('SquareGame', Category.aclass))
print(tbl.get_index('square', Category.field))
print(tbl.get_index('direction', Category.field))