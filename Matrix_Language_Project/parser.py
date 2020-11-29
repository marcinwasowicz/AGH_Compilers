import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("left", 'ADD', 'SUB'),
    ("left", 'MULT', 'DIV'),
    ("right", 'UNARY_SUB'),
    ("left", 'ARR_ADD', 'ARR_SUB'),
    ("left", 'ARR_MULT', 'ARR_DIV')
)

def p_general_expression(p):
    '''ex : BRACKET ex CLOSE_BRACKET
          | CURL_BRACKET ex CLOSE_CURL_BRACKET'''

def p_expression_evloution(p):
    '''ex : action SEPARATOR ex
          | action SEPARATOR
          | ifstatement ex
          | ifstatement
          | looping ex
          | looping'''

def p_action_evolution(p):
    '''action : assignement
              | PRINT sequence
              | CONTINUE
              | BREAK
              | RETURN operation'''

def p_ifstatement_evolution(p):
    '''ifstatement : IF condition ex
                   | IF condition ex elseifstatement'''

def p_elseifstatement_evolution(p):
    '''elseifstatement : ELSE IF condition ex 
                       | ELSE IF condition ex elseifstatement
                       | ELSE ex'''

def p_looping_evolution(p):
    '''looping : while_looping
               | for_looping'''

def p_while_looping_evolution(p):
    '''while_looping : WHILE condition ex'''

def p_for_looping_evolution(p):
    '''for_looping : FOR ID ASSIGN operation RANGE operation ex'''

def p_assignement_evolution(p):
    '''assignement : lvalue ASSIGN operation
                   | lvalue ADD_ASSIGN operation
                   | lvalue SUB_ASSIGN operation
                   | lvalue MULT_ASSIGN operation
                   | lvalue DIV_ASSIGN operation
                   | lvalue ASSIGN STRING'''

def p_lvalue_evolution(p):
    '''lvalue : ID
              | matrix_element'''

def p_matrix_element_evolution(p):
    '''matrix_element : ID SQ_BRACKET sequence CLOSE_SQ_BRACKET'''

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
            | ZEROS BRACKET INTEGER CLOSE_BRACKET
            | EYE BRACKET INTEGER CLOSE_BRACKET
            | ONES BRACKET INTEGER CLOSE_BRACKET'''

def p_inner_list_evolution(p):
    '''inner_list : list COMA inner_list
                  | SQ_BRACKET sequence CLOSE_SQ_BRACKET'''

def p_list_evolution(p):
    '''list : inner_list
            | SQ_BRACKET list CLOSE_SQ_BRACKET'''

def p_sequence_evolution(p):
    '''sequence : term
                | term COMA sequence'''

def p_condition_evolution(p):
    '''condition : BRACKET condition CLOSE_BRACKET
                 | BRACKET operation EQ operation CLOSE_BRACKET
                 | BRACKET operation NEQ operation CLOSE_BRACKET
                 | BRACKET operation LS operation CLOSE_BRACKET
                 | BRACKET operation GR operation CLOSE_BRACKET
                 | BRACKET operation LQ operation CLOSE_BRACKET
                 | BRACKET operation GQ operation CLOSE_BRACKET'''

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

parser = yacc.yacc()
