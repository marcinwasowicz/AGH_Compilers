from symbol_table import SymbolTable
from type_checker import TypeChecker

import sys
import scanner
import parser
import tree_printer


if __name__ == '__main__':
    text = open(sys.argv[1]).read()
    ast = parser.parser.parse(input=text, lexer=scanner.lexer)
    type_checker = TypeChecker(SymbolTable())
    errors = type_checker.visit(ast)
