import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from frontend import AST

types_dict = {
    AST.Integer.__name__: 'int',
    AST.Float.__name__: 'double',
    AST.String.__name__: 'char*'
}

print_dict = {
    AST.Integer.__name__: '%d',
    AST.Float.__name__: '%lf',
    AST.String.__name__: '%s'
}

keyword_dict = {
    'break': lambda continuation, cont_type, indent: '\t' * indent + 'break' + ';\n',
    'continue': lambda continuation, cont_type, indent: '\t' * indent + 'continue' + ';\n',
    'return': lambda continuation,  cont_type, indent: '\t' * indent + 'return ' + continuation + ';\n',
    'print': lambda continuation, cont_type, indent: '\t' * indent + 
        'printf(' + '"' + " ".join([print_dict[elem] for elem in cont_type ]) + '\\n"' + ', ' +  continuation + ');\n'
}

libraries = [
    '#include <stdio.h>',
    '#include <stdlib.h>',
    '#include <stdbool.h>',
    '#include "matrix_lib.h"'
]

def resolve_printf(continuation, cont_type, indent):
   # todo implement matrix printing!
   pass

def for_loop_to_string(iterator, iter_type, start, end, body, indent):
    result = '\t' * indent + 'for(' + types_dict[iter_type] + ' ' + iterator +  ' = ' + start + '; '
    result += iterator + ' < ' + end + '; ' + iterator + '++){\n'
    result += body + '\t' * indent + '}\n'
    return result

def while_loop_to_string(condition, body, indent):
    result = '\t' * indent + 'while(' + condition + '){\n'
    result += body + '\t' * indent + '}\n'
    return result

def if_to_string(condition, body, indent):
    return '\t' * indent + 'if (' + condition + '){\n' + body + '\t' * indent + '}\n'

def else_to_string(body, indent):
    return '\t' * indent + 'else' + ' ' + '{\n' + body + '\t' * indent + '}\n'

def decorate(generated_code):
    headers = str()
    for library in libraries:
        headers += library + '\n'

    generated_code = 'int main() {\n' + generated_code + '\treturn 0;\n}\n'
    return headers + generated_code
