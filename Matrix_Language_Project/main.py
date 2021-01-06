import sys
sys.dont_write_bytecode = True

from frontend import symbol_table
from frontend import type_checker
from frontend import scanner
from frontend import parser
from frontend import tree_printer
from c_code_generation import generator

if __name__ == '__main__':
    text = open(sys.argv[1], 'r').read()
    ast = parser.parser.parse(input=text, lexer=scanner.lexer, tracking=True)
    type_checker = type_checker.TypeChecker(symbol_table.SymbolTable())
    errors = type_checker.visit(ast)
    if errors:
        for error in errors:
            print(error)
        sys.exit("Compilation failed with: " + str(len(errors)) + " errors")
    else:
        code_generator = generator.CodeGenerator()
        c_code = code_generator.generate(ast)
        open(sys.argv[2], 'w+').write(c_code)

        
