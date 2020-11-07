import sys
import scanner
import parser

if __name__ == '__main__':

    text = open(sys.argv[1]).read()
    parser.parser.parse(input=text, lexer=scanner.lexer)