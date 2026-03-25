reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'def': 'DEF',
    'return': 'RETURN',
}

tokens = ['NUMBER', 'MINUS', 'PLUS', 'TIMES', 'DIVIDE', 'LPAREN',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP',
          'EGALEGAL', 'INFEG', 'SUPEG','NOTEG', 'LACC', 'RACC', 'COMMA', 'STRING','REF'] + list(reserved.values())

t_REF = r'\&'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_SEMI = r';'
t_EGAL = r'\='
t_INF = r'\<'
t_SUP = r'\>'
t_SUPEG = r'\>\='
t_INFEG = r'\<\='
t_EGALEGAL = r'\=\='
t_NOTEG = r'\!\='
t_LACC = r'\{'
t_RACC = r'\}'
t_COMMA = r'\,'


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    return t

# def t_POINTER(t):
#     r'\*[a-zA-Z_][a-zA-Z_0-9]*'
#     t.type = reserved.get(t.value, 'POINTER')  # Check for reserved words
#     return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = str(t.value[1:-1])
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lexer = lex.lex()
