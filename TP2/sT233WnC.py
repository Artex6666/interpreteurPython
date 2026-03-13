# -*- coding: utf-8 -*-
from genereTreeGraphviz2 import printTreeGraph

reserved={
        'print':'PRINT',
        'if': 'IF',
        'for': 'FOR',
        'while':'WHILE',
        'def': 'DEF',
        'return': 'RETURN'
        }

tokens = [ 'NUMBER','MINUS', 'PLUS','TIMES','DIVIDE', 'LPAREN',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP',
          'EGALEGAL','INFEG','LACC','RACC','COMMA']+ list(reserved.values())

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
#t_NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_INF = r'\<'
t_SUP = r'>'
t_INFEG = r'\<\='
t_EGALEGAL = r'\=\='
t_LACC = r'\{'
t_RACC = r'\}'
t_COMMA = r'\,'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t


def t_NUMBER(t): 
    r'\d+' 
    t.value = int(t.value) 
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
import ply.lex as lex
lex.lex()

names={}
precedence = ( 
        ('left','OR' ), 
        ('left','AND'), 
        ('nonassoc', 'INF', 'INFEG', 'EGALEGAL', 'SUP'), 
        ('left','PLUS', 'MINUS' ), 
        ('left','TIMES', 'DIVIDE'), 
        )
stack = []
functions = {}
function_template = {
    "name": None,
    "param": None,
    "body": None
}

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

def evalInst(t) -> None:
    print('evalInst de ',t)
    if t == 'empty': return
    assert type(t) is tuple
    if t[0] == 'bloc':
        evalInst(t[1])
        evalInst(t[2])
    if t[0] == 'print': print('CALC>', evalExpr(t[1]))
    if t[0] == 'if':
        evalExpr(t[1])
        if evalExpr(t[1]):
            evalInst(t[2])
    if t[0] == 'for':
        evalInst(t[1])
        while evalExpr(t[2]):
            evalInst(t[4])
            evalInst(t[3])
            
    if t[0] == 'while':
        while evalExpr(t[1]):
            evalInst(t[2])
            
    if t[0] == 'assign':
        names[t[1]] = evalExpr(t[2])
        return
    if t[0] == 'def':
        f = function_template.copy()
        f["name"] = t[1]
        f["param"] = flatten_params(t[2])
        f["body"] = t[3]

        functions[f["name"]] = f
        return
    if t[0] == 'return':
        value = evalExpr(t[1])
        raise ReturnSignal(value)

    if t[0] == 'call':
        return evalCall(t)


    
def flatten_params(t):
    if len(t) == 2:
        return [t[1]]
    else:
        return [t[1]] + flatten_params(t[2])

def evalCall(t):
    name = t[1]
    args = t[2]

    fun = fun = functions[name]
    params = fun["param"]
    body = fun["body"]

    frame = {}
    for p, a in zip(params, args):
        frame[p] = evalExpr(a)

    stack.append(frame)
    try:
        evalInst(body)
        return None
    except ReturnSignal as r:
        return r.value
    finally:
        stack.pop()


def evalExpr(t) -> int:
    print('evalExpr de ',t)
    if type(t) == int: return t
    if type(t) == str: return names[t]
    if type(t) == tuple :
        if t[0] == '+': return evalExpr(t[1]) + evalExpr(t[2])
        if t[0] == '-': return evalExpr(t[1]) - evalExpr(t[2])
        if t[0] == '*': return evalExpr(t[1]) * evalExpr(t[2])
        if t[0] == '/': return evalExpr(t[1]) // evalExpr(t[2])
        if t[0] == '>': return evalExpr(t[1]) > evalExpr(t[2])
        if t[0] == '<': return evalExpr(t[1]) < evalExpr(t[2])
        if t[0] == '==': return evalExpr(t[1]) == evalExpr(t[2])
        if t[0] == '<=': return evalExpr(t[1]) <= evalExpr(t[2])
        if t[0] == '>': return evalExpr(t[1]) > evalExpr(t[2])
        if t[0] == '||': return evalExpr(t[1]) or evalExpr(t[2])
        if t[0] == '&&': return evalExpr(t[1]) and evalExpr(t[2])
        

def p_start(p):
    'start : bloc'
    print(p[1])
    printTreeGraph(p[1])
    evalInst(p[1])

def p_bloc(p):
    '''bloc : bloc statement SEMI
    | statement SEMI'''
    if len(p)==4  : 
        p[0] = ('bloc', p[1], p[2])
    else : 
        p[0] = ('bloc', 'empty', p[1])

def p_params_single(p):
    'params : NAME'
    p[0] = ('params',p[1])

def p_params_list(p):
    'params : NAME COMMA params'
    p[0] = ('params',p[1], p[3])



def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LACC bloc RACC'
    p[0] = ('if',p[3],p[6])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LACC bloc RACC'
    p[0] = ('while',p[3],p[6])

def p_statement_for(p):
    'statement : FOR LPAREN statement SEMI expression SEMI statement RPAREN LACC bloc RACC'
    p[0] = ('for', p[3], p[5], p[7], p[10]) # ('for',('assign','i',3),('<', x, 6),('+','i',1),('print',1))

def p_statement_expr(p): 
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print', p[3])
    #print(p[3]) 
    
def p_statement_assign(p):
    'statement : NAME EGAL expression'
    #names[p[1]]=p[3]
    p[0] = ('assign', p[1], p[3])
    #print(p[1], 'a été modifié')

def p_statement_function(p):
    'statement : DEF NAME LPAREN params RPAREN LACC bloc RACC'
    p[0] = ('def',p[2],p[4],p[7])

def p_statement_return(p):
    'statement : RETURN expression'
    p[0] = ('return', p[2])

def p_expression_binop_inf(p): 
    'expression : expression INF expression' 
    #p[0] = p[1] < p[3] 
    p[0] = ('<',p[1],p[3])

def p_expression_binop_infEGAL(p): 
    'expression : expression INFEG expression' 
    #p[0] = p[1] <= p[3]
    p[0] = ('<=',p[1],p[3])

def p_expression_binop_sup(p): 
    'expression : expression SUP expression' 
    #p[0] = p[1] > p[3] 
    p[0] = ('>',p[1],p[3])
    
def p_expression_binop_egal(p): 
    'expression : expression EGALEGAL expression' 
    #p[0] = p[1] == p[3] 
    p[0] = ('==',p[1],p[3])

def p_expression_binop_and(p): 
    'expression : expression AND expression' 
    #p[0] = p[1] and p[3] 
    p[0] = ('&&',p[1],p[3])

def p_expression_binop_or(p): 
    'expression : expression OR expression' 
    #p[0] = p[1] or p[3]
    p[0] = ('||',p[1],p[3])

def p_expression_binop_plus(p): 
    'expression : expression PLUS expression' 
    #p[0] = p[1] + p[3] 
    p[0] = ('+', p[1], p[3])
    
def p_expression_binop_times(p): 
    'expression : expression TIMES expression' 
    #p[0] = p[1] * p[3] 
    p[0] = ('*', p[1], p[3])
    
def p_expression_binop_minus(p):
    'expression : expression MINUS expression'
    p[0] = ('-',p[1],p[3])

def p_expression_binop_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = ('/',p[1],p[3])
# def p_expression_binop_divide_and_minus(p): 
#     '''expression : expression MINUS expression 
#      | expression DIVIDE expression''' 
#     if p[2] == '-': p[0] = p[1] - p[3] 
#     else : p[0] = p[1] / p[3] 

def p_expression_call(p):
    'expression : NAME LPAREN params RPAREN'
    p[0] = ('call', p[1], p[3])

def p_expression_group(p): 
    'expression : LPAREN expression RPAREN' 
    p[0] = p[2] 
    
def p_expression_number(p): 
    'expression : NUMBER' 
    p[0] = p[1] 
    
def p_expression_name(p): 
    'expression : NAME' 
    #p[0] = names[p[1]]
    p[0] = p[1]
    
def p_error(p):    print("Syntax error in input!")
    
import ply.yacc as yacc
yacc.yacc()
s = 'def add(x, y) { return x + y; }; add(5,6);'
yacc.parse(s)