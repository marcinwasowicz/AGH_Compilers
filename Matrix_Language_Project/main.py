import sys
import scanner

if __name__ == '__main__':

    file = open(sys.argv[1], 'r')
    text = file.read()
    lexer = scanner.lexer  
    lexer.input(text) 

    while True:
        tok = lexer.token()
        if not tok: 
            break   
        print("(%d): %s(%s)" %(tok.lineno,tok.type, tok.value))