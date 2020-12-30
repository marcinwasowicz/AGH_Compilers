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
    AST.Float.__name__: '%f',
    AST.String.__name__: '%s'
}

keyword_dict = {
    'break': lambda continuation, cont_type, indent: '\t' * indent + 'break' + ';\n',
    'continue': lambda continuation, cont_type, indent: '\t' * indent + 'continue' + ';\n',
    'return': lambda continuation,  cont_type, indent: '\t' * indent + 'return ' + continuation + ';\n',
    'print': lambda continuation, cont_type, indent: '\t' * indent + 
        'printf(' + '"' + " ".join([print_dict[elem] for elem in cont_type ]) + '\\n"' + ', ' +  continuation + ');\n'
}

def eye_to_diagonal(eye, size):
    idxs = set([i * size + i for i in range(size)])
    zero_count = 0
    eye = list(eye)
    for char_idx, char in enumerate(eye):
        if char == '0':
            if zero_count in idxs:
                eye[char_idx] = '1'
            zero_count += 1
    return "".join(eye)

matrix_initializers_dict = {
    'zeros': lambda size, indent: '{\n' + ('\t' * (indent + 1) + '{' + '0, ' * (size -1) + '0' + '},\n') * (size - 1) + 
        ('\t' * (indent + 1) + '{' + '0, ' * (size -1) + '0' + '}\n') + '\t' * indent + '}',

    'ones': lambda size, indent: '{\n' + ('\t' * (indent + 1) + '{' + '1, ' * (size -1) + '1' + '},\n') * (size - 1) + 
        ('\t' * (indent + 1) + '{' + '1, ' * (size -1) + '1' + '}\n') + '\t' * indent + '}',

    'eye': lambda size, indent: eye_to_diagonal(
        '{\n' + ('\t' * (indent + 1) + '{' + '0, ' * (size -1) + '0' + '},\n') * (size - 1) + 
        ('\t' * (indent + 1) + '{' + '0, ' * (size -1) + '0' + '}\n') + '\t' * indent + '}', size)
}

libraries = [
    '#include <stdio.h>',
    '#include <stdlib.h>'
]

def get_matrix_dimensions(matrix: list):
    matrix_dimensions = str()
   
    while isinstance(matrix, list):
        matrix_dimensions += '[' + str(len(matrix)) + ']'
        matrix = matrix[0]
        
    return matrix_dimensions

def get_matrix_dominant_type(matrix: list):
    while isinstance(matrix, list):
        matrix = matrix[0]

    if AST.Float.__name__ in matrix:
        return types_dict[AST.Float.__name__]
    return types_dict[AST.Integer.__name__]

def resolve_operation(left_side, left_type, right_side, right_type, operator):
    if not isinstance(left_type, list) and not isinstance(right_type, list):
        return left_side + ' ' + operator + ' ' + right_side

def indexing_sequence_to_string(indexing_sequence):
    result = str()
    for element in indexing_sequence:
        result += '[' + element + ']'
    return result

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




    
