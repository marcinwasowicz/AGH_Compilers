import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from frontend import AST
from frontend import symbol_table

MATRIX_TYPE = 'matrix*'
MATRIX_INIT = 'init_matrix_list('
DOUBLE_PTR = '(double*)'
INT_PTR = '(int*)'
MATRIX_ELEM_GET = 'get_element('

matrix_assignement_dict = {
    '+=': lambda store, data, _: 'add_elem_by_elem_store(' + store + ', ' + data + ');\n',
    '-=': lambda store, data, _: 'sub_elem_by_elem_store(' + store + ', ' + data + ');\n',
    '*=': lambda store, data, _: 'mult_elem_by_elem_store(' + store + ', ' + data + ');\n',
    '/=': lambda store, data, _: 'div_elem_by_elem_store(' + store + ', ' + data + ');\n',
    '=': lambda store, data, size: 'store(' + store + ', ' + matrix_init(size, data) + ');\n'
}

matrix_operation_dict = {
    '.+': lambda left, right: 'add_elem_by_elem(' + left + ', ' + right + ')',
    '.-': lambda left, right: 'sub_elem_by_elem(' + left + ', ' + right + ')',
    '.*': lambda left, right: 'mult_elem_by_elem(' + left + ', ' + right + ')',
    './': lambda left, right: 'div_elem_by_elem(' + left + ', ' + right + ')',
    "'": lambda left, _: 'transpose(' + left + ')',
    '*': lambda left, right: 'mult(' + left + ', ' + right + ')'
}

matrix_initializers_dict = {
    'zeros': lambda size: 'zeros(' + str(size) +')',
    'ones': lambda size: 'ones(' + str(size) +')',
    'eye': lambda size: 'eye(' + str(size) +')'
}

matrix_element_assignment_dict = {
    '=': lambda element, value: 'set_element(' + element[len(MATRIX_ELEM_GET):-1] + ', ' + value+ ');\n',
    '+=': lambda element, value: 'add_to_element(' + element[len(MATRIX_ELEM_GET):-1] + ', ' + value+ ');\n',
    '-=': lambda element, value: 'sub_from_element(' + element[len(MATRIX_ELEM_GET):-1] + ', ' + value+ ');\n',
    '*=': lambda element, value: 'mult_element_by(' + element[len(MATRIX_ELEM_GET):-1] + ', ' + value+ ');\n',
    '/=': lambda element, value: 'div_element_by(' + element[len(MATRIX_ELEM_GET):-1] + ', ' + value+ ');\n'
}

def get_matrix_dimensions(matrix: list):
    matrix_dimensions = str()
   
    while isinstance(matrix, list):
        matrix_dimensions += '[' + str(len(matrix)) + ']'
        matrix = matrix[0]
        
    return matrix_dimensions

def matrix_init(type_size, matrix_rep):
    if matrix_rep is None or type_size is None:
        return
    if matrix_rep[0] != '{':
        return matrix_rep
    dim = []
    while isinstance(type_size, list):
        dim.append(str(len(type_size)))
        type_size = type_size[0]
        dim_size = len(dim)
    dim = '{' + ', '.join(dim) + '}'
    matrix_rep = list(matrix_rep)[1:-1]
    matrix_rep = '{' + ', '.join([char for char in matrix_rep if char not in ['{', '}', ',', ' ']]) + '}'
    return MATRIX_INIT + ', '.join([DOUBLE_PTR + matrix_rep, INT_PTR + dim, str(dim_size)]) + ')'

def resolve_matrix_element_assignment(resolved_matrix_element,value, operator):
    return matrix_element_assignment_dict[operator](resolved_matrix_element, value)

def resolve_matrix_element_dereference(resolved_matrix_element):
    return MATRIX_ELEM_GET + resolved_matrix_element + ')'

def resolve_matrix_assignment(symbol_table: symbol_table.SymbolTable, name, right_side, operator, type_size):
    if symbol_table.get(name) is None:
        symbol_table.put(name, type_size)
        right_side = matrix_init(type_size, right_side)
        return ' '.join([MATRIX_TYPE, name, operator, right_side]) + ';\n'
    else:
        return matrix_assignement_dict[operator](name, right_side, type_size)

def resolve_matrix_operation(left_side,left_type, operator, right_side, right_type):
    left_side = matrix_init(left_type, left_side)
    right_side = matrix_init(right_type, right_side)
    return matrix_operation_dict[operator](left_side, right_side)
