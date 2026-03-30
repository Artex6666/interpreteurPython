from typing import Any

from ast_lang.node.binary_node import BinaryNode
from ast_lang.node.bool_node import BoolNode
from ast_lang.node.call_node import CallNode
from ast_lang.node.float_node import FloatNode
from ast_lang.node.number_node import NumberNode
from ast_lang.node.pointer_node import PointerNode
from ast_lang.node.pointer_param_node import PointerParamNode
from ast_lang.node.string_node import StringNode
from ast_lang.node.name_node import NameNode
from ast_lang.statement.assign_node import AssignNode
from ast_lang.statement.block_node import BlocKNode
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
from runtime.exception.division_by_zero_exception import DivisionByZeroException
from runtime.exception.name_exception import NameException
from runtime.exception.type_exception import TypeException
from runtime.frame import Frame
from runtime.reference import Reference
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

    if isinstance(node, PrintNode):
        value = eval_expr(node.content)

        if isinstance(value, Reference):
            print("CALC>", value)
        else:
            print("CALC>", value)

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
        frame = stack.top()
        name = node.name
        value = eval_expr(node.expr)

        if name in frame.locals:
            frame.set_local_var_value(name, value)
        else:
            frame.add_local_var(name, value)
        return

    if isinstance(node, PointerAssignNode):
        ref = stack.top().get_local_var_value(node.name)
        value = eval_expr(node.value)
        stack.set_var_value_in_parents(ref.value, value)
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
        raise TypeException(f"Function {name} expects {len(params)} args, got {len(args)}")

    frame = Frame(name, fun, args)

    for param, arg in zip(fun.params.args, args):
        if isinstance(param, PointerParamNode):
            frame.add_local_var(param.name, arg)
        elif isinstance(param, NameNode):
            frame.add_local_var(param.value, arg)
        else:
            raise TypeException("Unknown parameter type")

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
        return stack.get_var_value(node.value)

    if isinstance(node, RefNode):
        if stack.get_var_value(node.name):
            return Reference(node.name)

    if isinstance(node, StringNode):
        return node.string

    if isinstance(node,BoolNode):
        return node.value

    if isinstance(node, FloatNode):
        return node.number

    if isinstance(node, BinaryNode):
        left = eval_expr(node.left)
        right = eval_expr(node.right)
        op = node.op
        if op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            if type(left) != type(right):
                raise TypeException(f"unsupported operand type(s) for {op} : '{type(left).__name__}' and '{type(right).__name__}'")
            return left + right
        if op == '-':
            if type(left) != type(right):
                raise TypeException(f"unsupported operand type(s) for {op} : '{type(left).__name__}' and '{type(right).__name__}'")
            return left - right
        if op == '*':
            if type(left) != type(right):
                raise TypeException(f"unsupported operand type(s) for {op}: '{type(left).__name__}' and '{type(right).__name__}'")
            return left * right
        if op == '/':
            if right == 0:
                raise DivisionByZeroException("division by zero")
            if type(left) != type(right):
                raise TypeException(f"unsupported operand type(s) for {op} : '{type(left).__name__}' and '{type(right).__name__}'")
            return left // right
        if op == '>':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'")
            return left > right
        if op == '<':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'")
            return left < right
        if op == '==':
            return left == right
        if op == '<=':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'")
            return left <= right
        if op == '>=':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'")
            return left >= right
        if op == '||': return left or right
        if op == '&&': return left and right
        if op == '!=': return left != right
        if op == '%':
            if type(left) != type(right):
                raise TypeException(f"not all arguments converted during string formatting")
            return left % right

    if isinstance(node, NumberNode):
        return node.number

    if isinstance(node, PointerNode):
        ref = stack.top().get_local_var_value(node.name)
        name = ref.value
        try:
            return stack.get_var_value_in_parents(name)
        except NameException:
            pass
        return stack.frames[0].locals[name]

    if isinstance(node, CallNode):
        return eval_call(node)
    return None
