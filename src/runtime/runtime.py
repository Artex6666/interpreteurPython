from typing import Any

from ast_lang.node.binary_node import BinaryNode
from ast_lang.node.call_node import CallNode
from ast_lang.node.number_node import NumberNode
from ast_lang.node.string_node import StringNode
from ast_lang.node.name_node import NameNode
from ast_lang.node.unary_node import UnaryNode
from ast_lang.statement.assign_node import AssignNode
from ast_lang.statement.block_node import BlocKNode
from ast_lang.statement.expression_node import ExpressionNode
from ast_lang.statement.for_node import ForNode
from ast_lang.statement.func_node import FuncNode
from ast_lang.statement.if_node import IfNode
from ast_lang.statement.print_node import PrintNode
from ast_lang.statement.return_node import ReturnNode
from ast_lang.statement.while_node import WhileNode
from runtime.frame import Frame
from runtime.return_signal import ReturnSignal
from runtime.stack import Stack


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

def eval_inst(node) -> None:
    #print('evalInst de ',node)

    if node == 'empty': return

    if isinstance(node, BlocKNode):
        eval_inst(node.first)
        eval_inst(node.second)

    if isinstance(node, PrintNode): print('CALC>', eval_expr(node.content))

    if isinstance(node, ExpressionNode):
        eval_expr(node.expr)
        return

    if isinstance(node, IfNode):
        if eval_expr(node.condition):
            eval_inst(node.block)
            return

        for elif_node in node.elif_list:
            if eval_expr(elif_node.condition):
                eval_inst(elif_node.block)
                return

        if node.else_block:
            eval_inst(node.else_block.block)

    if isinstance(node, ForNode):
        eval_inst(node.init)
        while eval_expr(node.cond):
            eval_inst(node.body)
            eval_inst(node.incr)

    if isinstance(node, WhileNode):
        while eval_expr(node.condition):
            eval_inst(node.block)

    if isinstance(node, AssignNode):
        value = eval_expr(node.expr)
        stack.top().add_local_var(node.name, value)
        return

    if isinstance(node, FuncNode):
        functions[node.func_name] = node
        return

    if isinstance(node, ReturnNode):
        value = eval_expr(node.expr)
        raise ReturnSignal(value)


def eval_call(call_func):
    name = call_func.func_name
    fun = functions.get(name)

    params = fun.params.args
    args = [eval_expr(a) for a in call_func.args.args]

    if len(params) != len(args):
        raise Exception(f"Function {name} expects {len(params)} args, got {len(args)}")

    frame = Frame(name, fun, args)
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

    if isinstance(node, StringNode):
        return node.string

    if isinstance(node, BinaryNode):
        left = eval_expr(node.left)
        right = eval_expr(node.right)
        op = node.op
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left // right
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '==': return left == right
        if op == '<=': return left <= right
        if op == '>': return left > right
        if op == '>=': return left >= right
        if op == '||': return left or right
        if op == '&&': return left and right
        if op == '!=': return left != right

    if isinstance(node, NumberNode):
        return node.number

    if isinstance(node, CallNode):
        return eval_call(node)
    return None
