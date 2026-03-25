from ast_lang.node.pointer_node import PointerNode
from ast_lang.node.pointer_param_node import PointerParamNode
from ast_lang.node.string_node import StringNode
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
from ast_lang.statement.pointer_assign_node import PointerAssignNode
from ast_lang.statement.print_node import PrintNode
from ast_lang.node.ref_node import RefNode
from ast_lang.statement.return_node import ReturnNode
from ast_lang.statement.while_node import WhileNode
from graph_ast.genereTreeGraphviz2 import print_tree_graph
from runtime.runtime import eval_inst
from grammar.lexer import * # noqa: F401

def p_start(p):
    'start : bloc'
    #print(p[1])
    print_tree_graph(p[1])
    eval_inst(p[1])


def p_empty(p):
    'empty :'
    pass


def p_bloc(p):
    '''bloc : bloc statement SEMI
    | statement SEMI'''
    if len(p) == 4:
        p[0] = BlocKNode(p[1], p[2])
    else:
        p[0] = BlocKNode(EmptyNode(), p[1])


def p_param_name(p):
    'param : NAME'
    p[0] = NameNode(p[1])


def p_param_pointer(p):
    'param : TIMES NAME'
    p[0] = PointerParamNode(p[2])


def p_params_empty(p):
    'params : '
    p[0] = ParamsNode([])


def p_params_single(p):
    'params : param'
    p[0] = ParamsNode([p[1]])


def p_params_list(p):
    'params : param COMMA params'
    p[0] = ParamsNode([p[1]] + p[3].children)


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
    )  # ('for',('assign','i',3),('<', x, 6),('+','i',1),('print',1))


def p_statement_expr(p):
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = PrintNode(p[3])


def p_statement_assign(p):
    'statement : NAME EGAL expression'
    p[0] = AssignNode(
        name=p[1],
        expr=p[3]
    )

def p_statement_pointer_assign(p):
    'statement : TIMES NAME EGAL expression'
    p[0] = PointerAssignNode(
        name=p[2],
        value=p[4]
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


def p_expression_ref(p):
    'expression : REF NAME'
    p[0] = RefNode(p[2])

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

def p_expression_binop_not_equal(p):
    'expression : expression NOTEG expression'
    p[0] = BinaryNode(op='!=',
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

def p_expression_pointer(p):
    'expression : TIMES NAME'
    p[0] = PointerNode(p[2])


def p_error(p):    print("Syntax error in input!")


import ply.yacc as yacc
parser = yacc.yacc()
