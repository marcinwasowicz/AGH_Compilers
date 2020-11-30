import sys
import scanner
import parser
import TreePrinter

if __name__ == '__main__':

    text = open(sys.argv[1]).read()
    ast = parser.parser.parse(input=text, lexer=scanner.lexer)
    ast.printTree()