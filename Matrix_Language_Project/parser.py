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
    '''assignement : assignable ASSIGN operation
                   | assignable ADD_ASSIGN operation
                   | assignable SUB_ASSIGN operation
                   | assignable MULT_ASSIGN operation
                   | assignable DIV_ASSIGN operation
                   | assignable ASSIGN STRING'''

def p_assignable_evolution(p):
    '''assignable : ID 
                  | ID SQ_BRACKET indexing_sequence CLOSE_SQ_BRACKET'''

def p_operation_evolution(p):
    '''operation : term
                 | operation TRANSPOSE
                 | BRACKET operation CLOSE_BRACKET
                 | operation ARR_ADD operation
                 | operation ARR_SUB operation
                 | operation ARR_MULT operation
                 | operation ARR_DIV operation
                 | operation ADD operation
                 | operation SUB operation
                 | operation DIV operation
                 | operation MULT operation'''

def p_term_evolution(p):
    '''term : assignable
            | BRACKET term CLOSE_BRACKET
            | ZEROS BRACKET INTEGER CLOSE_BRACKET
            | EYE BRACKET INTEGER CLOSE_BRACKET
            | ONES BRACKET INTEGER CLOSE_BRACKET
            | SUB term %prec UNARY_SUB
            | INTEGER
            | FLOAT
            | STRING
            | list'''

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
                          | printable_sequence COMA term'''

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
