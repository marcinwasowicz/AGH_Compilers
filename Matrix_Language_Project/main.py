from frontend import symbol_table
from frontend import type_checker
from frontend import scanner
from frontend import parser
from frontend import tree_printer

import sys


if __name__ == '__main__':
    text = open(sys.argv[1]).read()
    ast = parser.parser.parse(input=text, lexer=scanner.lexer, tracking=True)
    type_checker = type_checker.TypeChecker(symbol_table.SymbolTable())
    errors = type_checker.visit(ast)
    for error in errors:
        print(error)
