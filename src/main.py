# -*- coding: utf-8 -*-
from typing import Any

from ast_lang.node.StringNode import StringNode
from ast_lang.node.args_node import ArgsNode
from ast_lang.node.binary_node import BinaryNode
from ast_lang.node.call_node import CallNode
from ast_lang.node.group_node import GroupNode
from ast_lang.node.name_node import NameNode
from ast_lang.node.number_node import NumberNode
from ast_lang.node.params_node import ParamsNode
from ast_lang.statement.assign_node import AssignNode
from ast_lang.statement.block_node import BlocKNode
from ast_lang.statement.elif_node import ElifNode
from ast_lang.statement.else_node import ElseNode
from ast_lang.statement.empty_node import EmptyNode
from ast_lang.statement.expression_node import ExpressionNode
from ast_lang.statement.for_node import ForNode
from ast_lang.statement.func_node import FuncNode
from ast_lang.statement.if_node import IfNode
from ast_lang.statement.print_node import PrintNode
from ast_lang.statement.return_node import ReturnNode
from ast_lang.statement.while_node import WhileNode
from graph_ast.genereTreeGraphviz2 import print_tree_graph
from runtime.frame import Frame
from runtime.stack import Stack

reserved={
        'print':'PRINT',
        'if': 'IF',
        'elif': 'ELIF',
        'else': 'ELSE',
        'for': 'FOR',
        'while':'WHILE',
        'def': 'DEF',
        'return': 'RETURN'
        }

tokens = [ 'NUMBER','MINUS', 'PLUS','TIMES','DIVIDE', 'LPAREN',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP',
          'EGALEGAL','INFEG','SUPEG','LACC','RACC','COMMA','STRING']+ list(reserved.values())

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
t_SUPEG  = r'\>\='
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

def t_STRING(t):
    r'\"[a-zA-Z_][a-zA-Z_0-9]*\"'
    t.value = str(t.value)
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
stack = Stack()
global_frame = Frame("__global__", None, [])
stack.push(global_frame)
functions = {}


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

def eval_inst(node) -> None:
    #print('evalInst de ',node)

    if node == 'empty': return

    if isinstance(node,BlocKNode):
        eval_inst(node.first)
        eval_inst(node.second)

    if isinstance(node,PrintNode): print('CALC>', eval_expr(node.content))

    if isinstance(node, ExpressionNode):
        eval_expr(node.expr)
        return

    if isinstance(node,IfNode):
        if eval_expr(node.condition):
            eval_inst(node.block)
            return

        for elif_node in node.elif_list:
            if eval_expr(elif_node.condition):
                eval_inst(elif_node.block)
                return

        if node.else_block:
            eval_inst(node.else_block.block)

    if isinstance(node,ForNode):
        eval_inst(node.init)
        while eval_expr(node.cond):
            eval_inst(node.body)
            eval_inst(node.incr)
            
    if isinstance(node,WhileNode):
        while eval_expr(node.condition):
            eval_inst(node.block)

    if isinstance(node, AssignNode):
        value = eval_expr(node.expr)
        stack.top().add_local_var(node.name, value)
        return

    if isinstance(node,FuncNode):
        functions[node.func_name] = node
        return

    if isinstance(node,ReturnNode):
        value = eval_expr(node.expr)
        raise ReturnSignal(value)

def eval_call(call_func):
    name = call_func.func_name
    fun = functions.get(name)

    params = fun.params.args
    args = [eval_expr(a) for a in call_func.args.args]

    if len(params) != len(args):
        raise Exception(f"Function {name} expects {len(params)} args, got {len(args)}")

    frame = Frame(name,fun,args)
    for param_name, arg_value in zip(fun.params.args, args):
        frame.add_local_var(param_name.value, arg_value)

    stack.push(frame)
    try:
        eval_inst(fun.body)
    except ReturnSignal as r:
        return r.value
    finally:
        stack.pop()

def eval_expr(node) -> None | int | bool | Any:
    #print('evalExpr de ',node)

    if isinstance(node, NameNode):
        return stack.top().get_local_var(node.value)

    if isinstance(node,StringNode):
        return node.string

    if isinstance(node,BinaryNode):
        left = eval_expr(node.left)
        right = eval_expr(node.right)
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
        if op == '>=': return left >= right
        if op == '||': return left or right
        if op == '&&': return left and right

    if isinstance(node, NumberNode):
        return node.number

    if isinstance(node,CallNode):
        return eval_call(node)
    return None


def p_start(p):
    'start : bloc'
    print(p[1])
    print_tree_graph(p[1])
    eval_inst(p[1])

def p_empty(p):
    'empty :'
    pass

def p_bloc(p):
    '''bloc : bloc statement SEMI
    | statement SEMI'''
    if len(p)==4: 
        p[0] = BlocKNode(p[1], p[2])
    else : 
        p[0] = BlocKNode(EmptyNode(), p[1])

def p_params_empty(p):
    'params : '
    p[0] = ParamsNode(EmptyNode())

def p_params_single(p):
    'params : NAME'
    p[0] = ParamsNode([NameNode(p[1])])

def p_params_list(p):
    'params : NAME COMMA params'
    p[0] = ParamsNode([NameNode(p[1])] + p[3].children)

def p_elif_list(p):
    '''
    elif_list : empty
          | ELIF LPAREN expression RPAREN LACC bloc RACC elif_list
    '''

    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [ElifNode(p[3], p[6])] + p[8]


def p_else_opt(p):
    '''
    else_opt : empty
         | ELSE LACC bloc RACC
    '''

    if len(p) == 2:
        p[0] = None
    else:
        p[0] = ElseNode(p[3])


def p_statement_if(p):
    '''
    statement : IF LPAREN expression RPAREN LACC bloc RACC elif_list else_opt
    '''
    p[0] = IfNode(
        condition=p[3],
        block=p[6],
        elif_list=p[8],
        else_block=p[9]
    )


def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LACC bloc RACC'
    p[0] = WhileNode(
        condition=p[3],
        block=p[6]
    )

def p_statement_for(p):
    'statement : FOR LPAREN statement SEMI expression SEMI statement RPAREN LACC bloc RACC'
    p[0] = ForNode(
        init=p[3],
        cond=p[5],
        incr=p[7],
        body=p[10]
    ) # ('for',('assign','i',3),('<', x, 6),('+','i',1),('print',1))

def p_statement_expr(p): 
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = PrintNode(p[3])
    
def p_statement_assign(p):
    'statement : NAME EGAL expression'
    p[0] = AssignNode(
        name=p[1],
        expr=p[3]
    )

def p_statement_function(p):
    'statement : DEF NAME LPAREN params RPAREN LACC bloc RACC'
    p[0] = FuncNode(
        func_name=p[2],
        params=p[4],
        body=p[7]
    )

def p_statement_return(p):
    'statement : RETURN expression'
    p[0] = ReturnNode(p[2])

def p_statement_expr_call(p):
    'statement : expression'
    p[0] = ExpressionNode(p[1])

def p_expression_binop_inf(p): 
    'expression : expression INF expression' 
    p[0] = BinaryNode(op='<',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_binop_infEGAL(p): 
    'expression : expression INFEG expression' 
    p[0] = BinaryNode(op='<=',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_binop_sup(p):
    'expression : expression SUPEG expression'
    p[0] = BinaryNode(op='>=',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_binop_supEGAL(p):
    'expression : expression SUP expression' 
    p[0] = BinaryNode(op='>',
                      left=p[1],
                      right=p[3]
                      )
    
def p_expression_binop_egal(p): 
    'expression : expression EGALEGAL expression' 
    p[0] = BinaryNode(op='==',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_binop_and(p): 
    'expression : expression AND expression' 
    p[0] = BinaryNode(op='&&',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_binop_or(p): 
    'expression : expression OR expression' 
    p[0] = BinaryNode(op='||',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_binop_plus(p): 
    'expression : expression PLUS expression' 
    p[0] = BinaryNode(op='+',
                      left=p[1],
                      right=p[3]
                      )
    
def p_expression_binop_times(p): 
    'expression : expression TIMES expression' 
    p[0] = BinaryNode(op='*',
                      left=p[1],
                      right=p[3]
                      )
    
def p_expression_binop_minus(p):
    'expression : expression MINUS expression'
    p[0] = BinaryNode(op='-',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_binop_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = BinaryNode(op='/',
                      left=p[1],
                      right=p[3]
                      )

def p_expression_call(p):
    'expression : NAME LPAREN args RPAREN'
    p[0] = CallNode(
        func_name=p[1],
        args=p[3]
    )

def p_args_empty(p):
    'args : '
    p[0] = ArgsNode([])

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

def p_expression_string(p):
    'expression : STRING'
    p[0] = StringNode(p[1])
    
def p_expression_name(p): 
    'expression : NAME' 
    p[0] = NameNode(p[1])

def p_error(p):    print("Syntax error in input!")


import ply.yacc as yacc
yacc.yacc()
s = 'def factoriel(x){ if(x == 0 || x == 1){ return 1;}; return x * factoriel(x-1);}; print(factoriel(5)); '
yacc.parse(s)
