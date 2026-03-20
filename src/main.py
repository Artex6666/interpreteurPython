# -*- coding: utf-8 -*-
from ast.node.args import ArgsNode
from ast.statement.block import BlocKNode
from ast.node.binary import BinaryNode
from ast.node.call import CallNode
from ast.node.params import ParamsNode
from ast.statement.assign_node import AssignNode
from ast.statement.for_node import ForNode
from ast.statement.func_node import FuncNode
from ast.statement.if_node import IfNode
from ast.statement.print_node import PrintNode
from ast.statement.return_node import ReturnNode
from ast.statement.while_node import WhileNode
from ast.node.name_node import NameNode
from ast.node.number_node import NumberNode
from ast.statement.expression_node import ExpressionNode
from ast.node.group_node import GroupNode
from ast.statement.empty_node import EmptyNode
from graph_ast.genereTreeGraphviz2 import printTreeGraph

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

def evalInst(node) -> None:
    print('evalInst de ',node)
    if node == 'empty': return
    if isinstance(node,BlocKNode):
        evalInst(node.first)
        evalInst(node.second)
    if isinstance(node,PrintNode): print('CALC>', evalExpr(node.content))
    if isinstance(node,IfNode):
        evalExpr(node.condition)
        if evalExpr(node.condition):
            evalInst(node.block)
    if isinstance(node,ForNode):
        evalInst(node.init)
        while evalExpr(node.cond):
            evalInst(node.body)
            evalInst(node.incr)
            
    if isinstance(node,WhileNode):
        while evalExpr(node.condition):
            evalInst(node.block)
            
    if isinstance(node,AssignNode):
        names[node.name] = evalExpr(node.expr)
        return
    if isinstance(node,FuncNode):
        f = function_template.copy()
        f["name"] = node.name
        f["param"] = flatten_params(node.params)
        f["body"] = node.bloc

        functions[f["name"]] = f
        return
    if isinstance(node,ReturnNode):
        value = evalExpr(node.expr)
        raise ReturnSignal(value)

    
def flatten_params(t):
    if len(t) == 2:
        return [t[1]]
    else:
        return [t[1]] + flatten_params(t[2])

def flatten_args(t):
    if len(t) == 1:
        return []
    if len(t) == 2:
        return [t[1]]
    return [t[1]] + flatten_args(t[2])

def evalCall(t):
    name = t[1]
    args = flatten_args(t[2])

    fun = functions[name]
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


def evalExpr(node) -> int:
    print('evalExpr de ',node)
   
    if type(node) == int: return node
    if type(node) == str: return names[node]
    if isinstance(node,BinaryNode):
        left = evalExpr(node.left)
        right = evalExpr(node.right)
        op = node.op
        if op == '+': return  left +  right 
        if op == '-': return  left -  right 
        if op == '*': return  left *  right 
        if op == '/': return  left // right 
        if op == '>': return  left >  right 
        if op == '<': return  left <  right 
        if op == '==': return left == right  
        if op == '<=': return left <= right  
        if op == '>': return  left >  right 
        if op == '||': return left or right  
        if op == '&&': return left and right
    if isinstance(node,CallNode):
        return evalCall(node)
        

def p_start(p):
    'start : bloc'
    print(p[1])
    printTreeGraph(p[1])
    evalInst(p[1])

def p_bloc(p):
    '''bloc : bloc statement SEMI
    | statement SEMI'''
    if len(p)==4: 
        p[0] = BlocKNode(p[1], p[2])
    else : 
        p[0] = BlocKNode(EmptyNode(), p[1])

def p_params_single(p):
    'params : NAME'
    p[0] = ParamsNode([NameNode(p[1])])

def p_params_list(p):
    'params : NAME COMMA params'
    p[0] = ParamsNode([NameNode(p[1])] + p[3].children)

def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LACC bloc RACC'
    p[0] = IfNode(p[3],p[6])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LACC bloc RACC'
    p[0] = WhileNode(p[3],p[6])

def p_statement_for(p):
    'statement : FOR LPAREN statement SEMI expression SEMI statement RPAREN LACC bloc RACC'
    p[0] = ForNode(p[3], p[5], p[7], p[10]) # ('for',('assign','i',3),('<', x, 6),('+','i',1),('print',1))

def p_statement_expr(p): 
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = PrintNode(p[3])
    
def p_statement_assign(p):
    'statement : NAME EGAL expression'
    p[0] = AssignNode(p[1], p[3])

def p_statement_function(p):
    'statement : DEF NAME LPAREN params RPAREN LACC bloc RACC'
    p[0] = FuncNode(p[2],p[4],p[7])

def p_statement_return(p):
    'statement : RETURN expression'
    p[0] = ReturnNode(p[2])

def p_statement_expr_call(p):
    'statement : expression'
    p[0] = ExpressionNode(p[1])

def p_expression_binop_inf(p): 
    'expression : expression INF expression' 
    p[0] = BinaryNode('<',p[1],p[3])

def p_expression_binop_infEGAL(p): 
    'expression : expression INFEG expression' 
    p[0] = BinaryNode('<=',p[1],p[3])

def p_expression_binop_sup(p): 
    'expression : expression SUP expression' 
    p[0] = BinaryNode('>',p[1],p[3])
    
def p_expression_binop_egal(p): 
    'expression : expression EGALEGAL expression' 
    p[0] = BinaryNode('==',p[1],p[3])

def p_expression_binop_and(p): 
    'expression : expression AND expression' 
    p[0] = BinaryNode('&&',p[1],p[3])

def p_expression_binop_or(p): 
    'expression : expression OR expression' 
    p[0] = BinaryNode('||',p[1],p[3])

def p_expression_binop_plus(p): 
    'expression : expression PLUS expression' 
    p[0] = BinaryNode('+',p[1],p[3])
    
def p_expression_binop_times(p): 
    'expression : expression TIMES expression' 
    p[0] = BinaryNode('*',p[1],p[3])
    
def p_expression_binop_minus(p):
    'expression : expression MINUS expression'
    p[0] = BinaryNode('-',p[1],p[3])

def p_expression_binop_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = BinaryNode('/',p[1],p[3])

def p_expression_call(p):
    'expression : NAME LPAREN args RPAREN'
    p[0] = CallNode(p[1], p[3])

def p_args_empty(p):
    'args : '
    p[0] = ArgsNode()

def p_args_single(p):
    'args : expression'
    p[0] = ArgsNode([p[1]])

def p_args_list(p):
    'args : expression COMMA args'
    p[0] = ArgsNode([p[1]] + p[3].children)


def p_expression_group(p): 
    'expression : LPAREN expression RPAREN' 
    p[0] = GroupNode(p[2]) 
    
def p_expression_number(p): 
    'expression : NUMBER' 
    p[0] = NumberNode(p[1]) 
    
def p_expression_name(p): 
    'expression : NAME' 
    p[0] = NameNode(p[1])
    


def p_error(p):    print("Syntax error in input!")


import ply.yacc as yacc
yacc.yacc()
s = 'def add(x, y) { return x + y; }; add(5,6); def sub(x,y) {return x - y;}; sub(6,5);'
yacc.parse(s)
 
