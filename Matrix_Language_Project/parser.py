import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("left", 'ADD', 'SUB'),
    ("left", 'MULT', 'DIV'),
    ("right", 'UNARY_SUB'),
    ("left", 'ARR_ADD', 'ARR_SUB'),
    ("left", 'ARR_MULT', 'ARR_DIV'),
    ("right", 'ELSE', 'THEN')
)

def p_program_evolution(p):
    '''program : actions'''

def p_actions_evolution(p):
    '''actions : block
               | actions block'''

def p_action_evolution(p):
    '''action : assignement SEPARATOR
              | ifstatement
              | for_looping
              | while_looping
              | PRINT sequence SEPARATOR
              | CONTINUE SEPARATOR
              | BREAK SEPARATOR
              | RETURN operation SEPARATOR'''

def p_assignement_evolution(p):
    '''assignement : lvalue ASSIGN operation
                   | lvalue ADD_ASSIGN operation
                   | lvalue SUB_ASSIGN operation
                   | lvalue MULT_ASSIGN operation
                   | lvalue DIV_ASSIGN operation'''

def p_lvalue_evolution(p):
    '''lvalue : ID
              | matrix_element'''

def p_matrix_element_evolution(p):
    '''matrix_element : ID list'''

def p_list_evolution(p):
    '''list : SQ_BRACKET sequence CLOSE_SQ_BRACKET'''

def p_sequence_evolution(p):
    '''sequence : sequence COMA operation
                | operation'''

def p_operation_evolution(p):
    '''operation : term
                 | BRACKET operation CLOSE_BRACKET
                 | operation ADD operation
                 | operation SUB operation
                 | operation MULT operation
                 | operation DIV operation
                 | operation ARR_ADD operation
                 | operation ARR_SUB operation
                 | operation ARR_MULT operation
                 | operation ARR_DIV operation
                 | operation TRANSPOSE'''

def p_term_evolution(p):
    '''term : BRACKET term CLOSE_BRACKET
            | SUB term %prec UNARY_SUB
            | lvalue
            | INTEGER
            | FLOAT
            | STRING
            | list
            | ZEROS BRACKET operation CLOSE_BRACKET
            | EYE BRACKET operation CLOSE_BRACKET
            | ONES BRACKET operation CLOSE_BRACKET'''

def p_ifstatement_evolution(p):
    '''ifstatement : IF condition block %prec THEN
                   | IF condition block ELSE block'''

def p_condition_evolution(p):
    '''condition : BRACKET condition CLOSE_BRACKET
                 | BRACKET operation EQ operation CLOSE_BRACKET
                 | BRACKET operation NEQ operation CLOSE_BRACKET
                 | BRACKET operation LS operation CLOSE_BRACKET
                 | BRACKET operation GR operation CLOSE_BRACKET
                 | BRACKET operation LQ operation CLOSE_BRACKET
                 | BRACKET operation GQ operation CLOSE_BRACKET'''

def p_block_evolution(p):
    '''block : CURL_BRACKET actions CLOSE_CURL_BRACKET
             | action'''

def p_while_looping_evolution(p):
    '''while_looping : WHILE condition block'''

def p_for_looping_evolution(p):
    '''for_looping : FOR ID ASSIGN operation RANGE operation block'''

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

parser = yacc.yacc()
