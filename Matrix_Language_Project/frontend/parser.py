from frontend import scanner 
from frontend import AST
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("right", 'ELSE'),
    ("left", 'ADD', 'SUB'),
    ("left", 'MULT', 'DIV'),
    ("left", 'ARR_ADD', 'ARR_SUB'),
    ("left", 'ARR_MULT', 'ARR_DIV'),
    ("left", 'TRANSPOSE'),
    ("right", 'UNARY_SUB'),
)

def p_program_evolution(p):
    '''program : actions'''
    p[0] = p[1]

def p_actions_evolution(p):
    '''actions : block
               | actions block'''
    if len(p) == 2:
        p[0] = AST.Actions(series=[p[1]])
    else:
        p[0] = AST.Actions(series=[p[1], p[2]])

def p_action_evolution(p):
    '''action : assignement SEPARATOR
              | ifstatement
              | for_looping
              | while_looping'''
    p[0] = p[1]

def p_action_evolution_keyword_instruction(p):
    '''action : PRINT sequence SEPARATOR
              | CONTINUE SEPARATOR
              | BREAK SEPARATOR
              | RETURN operation SEPARATOR'''
    p[0] = AST.KeyWordInstruction(keyword=p[1], continuation=p[2] if len(p) > 3 else None, lineno=p.lineno(1))

def p_assignement_evolution(p):
    '''assignement : lvalue ASSIGN operation
                   | lvalue ADD_ASSIGN operation
                   | lvalue SUB_ASSIGN operation
                   | lvalue MULT_ASSIGN operation
                   | lvalue DIV_ASSIGN operation'''
    p[0] = AST.Assignment(lvalue=p[1], operator=p[2], operation=p[3], lineno=p.lineno(2))

def p_lvalue_evolution_variable(p):
    '''lvalue : ID'''
    p[0] = AST.Variable(name=p[1], lineno=p.lineno(1))

def p_lvalue_evolution_matrix_element(p):
    '''lvalue : matrix_element'''
    p[0] = p[1]

def p_matrix_element_evolution(p):
    '''matrix_element : ID SQ_BRACKET sequence CLOSE_SQ_BRACKET'''
    p[0] = AST.MatrixElement(identifier=AST.Variable(name=p[1], lineno=p.lineno(1)), indexing_sequence=p[3], lineno=p.lineno(1))
    
def p_list_evolution(p):
    '''list : SQ_BRACKET sequence CLOSE_SQ_BRACKET'''
    p[0] = AST.List(sequence=p[2], lineno=p.lineno(1))

def p_sequence_evolution(p):
    '''sequence : operation COMA sequence
                | operation'''
    p[0] = AST.Sequence(elements=[p[1]] + p[3].elements if len(p) > 3 and p[3].elements is not None else [p[1]])

def p_operation_evolution(p):
    '''operation : term
                 | BRACKET operation CLOSE_BRACKET'''
    p[0] = p[1] if len(p) == 2 else p[2]

def p_operation_evolution_with_operators(p):
    '''operation : operation ADD operation
                 | operation SUB operation
                 | operation MULT operation
                 | operation DIV operation
                 | operation ARR_ADD operation
                 | operation ARR_SUB operation
                 | operation ARR_MULT operation
                 | operation ARR_DIV operation
                 | operation TRANSPOSE'''
    p[0] = AST.Operation(operator=p[2], left=p[1], right=p[3] if len(p) > 3 else None, lineno=p.lineno(2))
    
def p_term_evolution(p):
    '''term : BRACKET term CLOSE_BRACKET'''
    p[0] = p[2]

def p_term_evolution_unarysub(p):
    '''term : SUB term %prec UNARY_SUB'''
    p[0] = AST.UnaryVariable(operator=p[1], value=p[2])

def p_term_evolution_nonterminal(p):
    '''term : lvalue
            | list'''
    p[0] = p[1]

def p_term_evolution_integer(p):
    '''term : INTEGER'''
    p[0] = AST.Integer(value=p[1])

def p_term_evolution_float(p):
    '''term : FLOAT'''
    p[0] = AST.Float(value=p[1])

def p_term_evolution_string(p):
    '''term : STRING'''
    p[0] = AST.String(value=p[1])

def p_term_evoultion_matrix_initialization(p):
    '''term : ZEROS BRACKET operation CLOSE_BRACKET
            | EYE BRACKET operation CLOSE_BRACKET
            | ONES BRACKET operation CLOSE_BRACKET'''
    p[0] = AST.MatrixInitializer(keyword=p[1], operation=p[3], lineno=p.lineno(1))

def p_ifstatement_evolution(p):
    '''ifstatement : IF condition block
                   | IF condition block ELSE block'''
    p[0] = AST.IfStatement(condition=p[2], body=p[3], else_body=p[5] if len(p) > 5 else None)

def p_condition_evolution(p):
    '''condition : BRACKET condition CLOSE_BRACKET'''
    p[0] = p[2]

def p_condition_evolution_with_operator(p):
    '''condition : BRACKET operation EQ operation CLOSE_BRACKET
                 | BRACKET operation NEQ operation CLOSE_BRACKET
                 | BRACKET operation LS operation CLOSE_BRACKET
                 | BRACKET operation GR operation CLOSE_BRACKET
                 | BRACKET operation LQ operation CLOSE_BRACKET
                 | BRACKET operation GQ operation CLOSE_BRACKET'''
    p[0] = AST.Condition(operator=p[3], left=p[2], right=p[4], lineno=p.lineno(3))
    
def p_block_evolution(p):
    '''block : CURL_BRACKET actions CLOSE_CURL_BRACKET
             | action'''
    p[0] = AST.Actions(series=[p[1] if len(p) == 2 else p[2]])

def p_while_looping_evolution(p):
    '''while_looping : WHILE condition block'''
    p[0] = AST.WhileLooping(condition=p[2], body=p[3])

def p_for_looping_evolution(p):
    '''for_looping : FOR ID ASSIGN operation RANGE operation block'''
    p[0] = AST.ForLooping(iterator=AST.Variable(name = p[2], lineno=p.lineno(2)), start=p[4], end=p[6], body=p[7])

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

parser = yacc.yacc(debug=False, write_tables=False)
