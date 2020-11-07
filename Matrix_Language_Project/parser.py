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
    '''action : numeric_assignement
              | matrix_assignement
              | PRINT printable_sequence
              | CONTINUE
              | BREAK
              | RETURN returnable_statement'''

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
    '''for_looping : FOR ID ASSIGN numeric_operation RANGE numeric_operation ex'''

def p_matrix_assignement_evolution(p):
    '''matrix_assignement : ID ASSIGN matrix_operation'''

def p_numeric_assignement_evolution(p):
    '''numeric_assignement : ID ASSIGN numeric_operation
                           | ID ADD_ASSIGN numeric_operation
                           | ID SUB_ASSIGN numeric_operation
                           | ID MULT_ASSIGN numeric_operation
                           | ID DIV_ASSIGN numeric_operation
                           | matrix_element ASSIGN numeric_operation
                           | matrix_element ADD_ASSIGN numeric_operation
                           | matrix_element SUB_ASSIGN numeric_operation
                           | matrix_element MULT_ASSIGN numeric_operation
                           | matrix_element DIV_ASSIGN numeric_operation'''

def p_matrix_operation_evolution(p):
    '''matrix_operation : matrix_term
                        | matrix_operation TRANSPOSE
                        | BRACKET matrix_operation CLOSE_BRACKET
                        | matrix_operation ARR_ADD matrix_operation
                        | matrix_operation ARR_SUB matrix_operation
                        | matrix_operation ARR_MULT matrix_operation
                        | matrix_operation ARR_DIV matrix_operation'''

def p_numeric_operation_evolution(p):
    '''numeric_operation : numeric_term
                         | BRACKET numeric_operation CLOSE_BRACKET
                         | numeric_operation ADD numeric_operation
                         | numeric_operation SUB numeric_operation
                         | numeric_operation MULT numeric_operation
                         | numeric_operation DIV numeric_operation'''

def p_matrix_term_evolution(p):
    '''matrix_term : BRACKET matrix_term CLOSE_BRACKET
                   | ID
                   | ZEROS BRACKET INTEGER CLOSE_BRACKET
                   | EYE BRACKET INTEGER CLOSE_BRACKET
                   | ONES BRACKET INTEGER CLOSE_BRACKET
                   | list'''

def p_numeric_term_evolution(p):
    '''numeric_term : BRACKET numeric_term CLOSE_BRACKET
                    | SUB numeric_term %prec UNARY_SUB
                    | ID
                    | INTEGER
                    | FLOAT
                    | matrix_element'''

def p_matrix_element_evolution(p):
    '''matrix_element : ID SQ_BRACKET sequence CLOSE_SQ_BRACKET'''

def p_list_evolution(p):
    '''list : inner_list
            | SQ_BRACKET list CLOSE_SQ_BRACKET'''

def p_inner_list_evolution(p):
    '''inner_list : SQ_BRACKET sequence CLOSE_SQ_BRACKET
                  | list COMA inner_list'''

def p_sequence_evolution(p):
    '''sequence : ID
                | INTEGER
                | FLOAT
                | sequence COMA ID
                | sequence COMA FLOAT
                | sequence COMA INTEGER'''

def p_printable_sequence_evolution(p):
    '''printable_sequence : BRACKET printable_sequence CLOSE_BRACKET
                          | printable_sequence COMA ID
                          | printable_sequence COMA INTEGER
                          | printable_sequence COMA FLOAT
                          | printable_sequence COMA STRING
                          | INTEGER
                          | FLOAT
                          | list
                          | STRING
                          | ID'''

def p_condition_evolution(p):
    '''condition : BRACKET condition CLOSE_BRACKET
                 | BRACKET numeric_operation EQ numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation NEQ numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation LS numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation GR numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation LQ numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation GQ numeric_operation CLOSE_BRACKET'''

def p_returnable_statement(p):
    '''returnable_statement : numeric_operation
                            | matrix_operation
                            | STRING'''


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

parser = yacc.yacc()
