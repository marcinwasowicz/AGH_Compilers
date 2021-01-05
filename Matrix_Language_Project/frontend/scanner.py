import ply.lex as lex

tokens = [
    'ADD_ASSIGN', 'SUB_ASSIGN', 'MULT_ASSIGN', 'DIV_ASSIGN',
    'LQ', 'GQ', 'EQ', 'NEQ',
    'GR', 'LS', 'ASSIGN',
    'ARR_ADD', 'ARR_SUB', 'ARR_MULT', 'ARR_DIV',
    'ADD', 'SUB', 'MULT', 'DIV',
    'BRACKET', 'CLOSE_BRACKET', 'CURL_BRACKET', 'CLOSE_CURL_BRACKET', 'SQ_BRACKET', 'CLOSE_SQ_BRACKET',
    'TRANSPOSE', 'RANGE', 'SEPARATOR', 'COMA',
    'ID','FLOAT', 'INTEGER', 'STRING',
    'COMMENT'
]

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'break': 'BREAK',
    'return': 'RETURN',
    'continue': 'CONTINUE',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'while': 'WHILE',
    'print': 'PRINT',
    'for': 'FOR'
}

tokens += list(reserved.values())

def t_ADD_ASSIGN(t):
    r'\+='
    return t

def t_SUB_ASSIGN(t):
    r'\-='
    return t

def t_MULT_ASSIGN(t):
    r'\*='
    return t

def t_DIV_ASSIGN(t):
    r'\/='
    return t

def t_LQ(t):
    r'<='
    return t

def t_GQ(t):
    r'>='
    return t

def t_EQ(t):
    r'=='
    return t

def t_NEQ(t):
    r'!='
    return t

def t_GR(t):
    r'>'
    return t

def t_LS(t):
    r'<'
    return t

def t_ASSIGN(t):
    r'='
    return t

def t_ARR_ADD(t):
    r'\.\+'
    return t

def t_ARR_SUB(t):
    r'\.\-'
    return t

def t_ARR_MULT(t):
    r'\.\*'
    return t

def t_ARR_DIV(t):
    r'\.\/'
    return t

def t_ADD(t):
    r'\+'
    return t

def t_SUB(t):
    r'\-'
    return t

def t_MULT(t):
    r'\*'
    return t

def t_DIV(t):
    r'\/'
    return t

def t_FLOAT(t):
    r'((\d*\.\d+)|(\d+\.\d*))([eE][-+]?\d+)?'
    return t

def t_INTEGER(t):
    r'(0)|[1-9][0-9]*'
    return t

def t_TRANSPOSE(t):
    r'\''
    return t
    
def t_RANGE(t):
    r':'
    return t

def t_BRACKET(t):
    r'\('
    return t

def t_CLOSE_BRACKET(t):
    r'\)'
    return t

def t_CURL_BRACKET(t):
    r'\{'
    return t

def t_CLOSE_CURL_BRACKET(t):
    r'\}'
    return t

def t_SQ_BRACKET(t):
    r'\['
    return t

def t_CLOSE_SQ_BRACKET(t):
    r'\]'
    return t

def t_SEPARATOR(t):
    r';'
    return t

def t_COMA(t):
    r','
    return t

def t_ID(t) :
    r"[a-zA-Z_]\w*"
    t.type = reserved.get(t.value,'ID')
    return t

def t_STRING(t):
    r'".*?"'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
t_ignore  = ' \t'
 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
