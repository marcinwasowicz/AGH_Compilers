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
              | PRINT printable_sequence
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
    '''assignement : ID ASSIGN operation
                   | ID ADD_ASSIGN operation
                   | ID SUB_ASSIGN operation
                   | ID MULT_ASSIGN operation
                   | ID DIV_ASSIGN operation
                   | ID ASSIGN STRING
                   | matrix_element ASSIGN operation
                   | matrix_element ADD_ASSIGN operation
                   | matrix_element SUB_ASSIGN operation
                   | matrix_element MULT_ASSIGN operation
                   | matrix_element DIV_ASSIGN operation'''

def p_assignable_evolution(p):
    '''matrix_element : ID SQ_BRACKET indexing_sequence CLOSE_SQ_BRACKET'''

def p_operation_evolution(p):
    '''operation : numeric_operation
                 | matrix_operation'''

def p_numeric_operation_evolution(p):
    '''numeric_operation : numeric_term
                         | BRACKET numeric_operation CLOSE_BRACKET
                         | numeric_operation ADD numeric_operation
                         | numeric_operation SUB numeric_operation
                         | numeric_operation DIV numeric_operation
                         | numeric_operation MULT numeric_operation'''

def p_matrix_operation_evolution(p):
    '''matrix_operation : matrix_term
                        | BRACKET matrix_operation CLOSE_BRACKET
                        | matrix_operation TRANSPOSE
                        | matrix_operation ARR_ADD matrix_operation
                        | matrix_operation ARR_SUB matrix_operation
                        | matrix_operation ARR_MULT matrix_operation
                        | matrix_operation ARR_DIV matrix_operation'''

def p_numeric_term_evolution(p):
    '''numeric_term : ID
                    | matrix_element
                    | INTEGER
                    | FLOAT
                    | BRACKET numeric_term CLOSE_BRACKET
                    | SUB term %prec UNARY_SUB'''

def p_matrix_term_evolution(p):
    '''matrix_term : ID
                   | ZEROS BRACKET INTEGER CLOSE_BRACKET
                   | EYE BRACKET INTEGER CLOSE_BRACKET
                   | ONES BRACKET INTEGER CLOSE_BRACKET
                   | list
                   | BRACKET matrix_term CLOSE_BRACKET'''

def p_term_evolution(p):
    '''term : numeric_term
            | matrix_term'''

def p_list_evolution(p):
    '''list : inner_list
            | SQ_BRACKET list CLOSE_SQ_BRACKET'''

def p_inner_list_evolution(p):
    '''inner_list : SQ_BRACKET array_sequence CLOSE_SQ_BRACKET
                  | list COMA inner_list'''

def p_array_sequence_evolution(p):
    '''array_sequence : INTEGER
                      | FLOAT
                      | array_sequence COMA INTEGER
                      | array_sequence COMA FLOAT'''

def p_indexing_sequence_evolution(p):
    '''indexing_sequence : INTEGER
                         | indexing_sequence COMA INTEGER'''

def p_printable_sequence_evolution(p):
    '''printable_sequence : term
                          | STRING
                          | printable_sequence COMA term
                          | printable_sequence COMA STRING'''

def p_condition_evolution(p):
    '''condition : BRACKET condition CLOSE_BRACKET
                 | BRACKET operation EQ operation CLOSE_BRACKET
                 | BRACKET operation NEQ operation CLOSE_BRACKET
                 | BRACKET numeric_operation LS numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation GR numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation LQ numeric_operation CLOSE_BRACKET
                 | BRACKET numeric_operation GQ numeric_operation CLOSE_BRACKET'''

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

parser = yacc.yacc()
