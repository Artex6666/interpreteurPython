# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------

tokens = ('SUP','INF','NAME','EQUAL','SEMI','AND', 'OR',
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE',
    'LPAREN','RPAREN'
    )

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_AND = r'\&'
t_OR = r'\|'
t_SEMI = r'\;'
t_EQUAL = r'\='
t_NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_INF = r'\<'
t_SUP = r'\>'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'

    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex

from TP2.genereTreeGraphviz2 import printTreeGraph
lex.lex()
names = {}

def p_start(p):
    'start: bloc'
    print(p[1])
    printTreeGraph(p[1])

def p_bloc(p):
    '''bloc : bloc statement SEMI 
    | statement SEMI'''
    if len(p) == 4:
        p[0] = ('bloc',p[1],p[2])
    else:
        p[0] = ('bloc',p[1],'Empty')

def p_statement_assign(p):
    'statement : NAME EQUAL expression'

def p_statement_expr(p):
    'statement : expression'
    p[0] = print(p[1])


def p_expression_binop_inf(p):
    'expression : expression INF expression'
    #p[0] = p[1] < p[3]
    p[0] = ('<',p[1],p[3])

def p_expression_binop_sup(p):
    'expression : expression SUP expression'
    #p[0] = p[1] > p[3]
    p[0] = ('>',p[1],p[3])

def p_expression_binop_and(p):
    'expression : expression AND expression'
    p[0] = p[1] and p[3]

def p_expression_binop_or(p):
    'expression : expression OR expression'
    p[0] = p[1] or p[3]

def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    #p[0] = p[1] + p[3]
    p[0] = ('+',p[1],p[3])

def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    p[0] = p[1] * p[3]

def p_expression_binop_divide_and_minus(p):
    '''expression : expression MINUS expression
				| expression DIVIDE expression'''
    if p[2] == '-': p[0] = p[1] - p[3]
    else : p[0] = p[1] / p[3]	
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

s = input('calc > ')
yacc.parse(s)

    