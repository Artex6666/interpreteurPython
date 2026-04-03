from typing import Any

from ast_lang.node.binary_node import BinaryNode
from ast_lang.node.bool_node import BoolNode
from ast_lang.node.call_node import CallNode
from ast_lang.node.float_node import FloatNode
from ast_lang.node.group_node import GroupNode
from ast_lang.node.number_node import NumberNode
from ast_lang.node.pointer_node import PointerNode
from ast_lang.node.pointer_param_node import PointerParamNode
from ast_lang.node.string_node import StringNode
from ast_lang.node.name_node import NameNode
from ast_lang.statement.assign_node import AssignNode
from ast_lang.statement.block_node import BlocKNode
from ast_lang.statement.expression_node import ExpressionNode
from ast_lang.statement.for_node import ForNode
from ast_lang.statement.func_node import FuncNode
from ast_lang.statement.if_node import IfNode
from ast_lang.statement.pointer_assign_node import PointerAssignNode
from ast_lang.statement.print_node import PrintNode
from ast_lang.node.ref_node import RefNode
from ast_lang.statement.return_node import ReturnNode
from ast_lang.statement.while_node import WhileNode
from runtime.exception.attribute_exception import AttributeException
from runtime.exception.division_by_zero_exception import DivisionByZeroException
from runtime.exception.name_exception import NameException
from runtime.exception.type_exception import TypeException
from runtime.frame import Frame
from runtime.reference import Reference
from runtime.return_signal import ReturnSignal
from runtime.stack import Stack
from runtime.trace.stack_trace import StackTrace
from runtime.trace.trace_frame import TraceFrame

names={}
precedence = (
        ('left','OR' ),
        ('left','AND'),
        ('nonassoc', 'INF', 'INFEG', 'EGALEGAL', 'SUP'),
        ('left','PLUS', 'MINUS' ),
        ('left','TIMES', 'DIVIDE'),
        )
stack = Stack()
stack_trace = StackTrace()
global_frame = Frame("__global__", None, [],stack_trace)
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
        if not ref:
            stack.top().add_local_var(node.name, value)
            return

        if not isinstance(ref, Reference):
            raise AttributeException(
                f"Cannot assign through non-pointer '{type(ref).__name__}'",
                stack_trace.copy()
            )

        stack.set_var_value_in_parents(ref.value, value,stack_trace)
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
    trace_frame = TraceFrame(name,call_func.args,call_func.line)

    if fun is None:
        raise AttributeException(f"function '{name}' is not defined",stack_trace.copy())

    stack_trace.push(trace_frame)

    params = fun.params.args
    args = [eval_expr(a) for a in call_func.args.args]

    if len(params) != len(args):
        raise TypeException(f"Function {name} expects {len(params)} args, got {len(args)}",stack_trace.copy())

    frame = Frame(name, fun, args,stack_trace.copy())

    for param, arg in zip(fun.params.args, args):
        if isinstance(param, PointerParamNode):
            frame.add_local_var(param.name, arg)
        elif isinstance(param, NameNode):
            frame.add_local_var(param.value, arg)
        else:
            raise TypeException("Unknown parameter type",stack_trace.copy())

    stack.push(frame)
    try:
        eval_inst(fun.body)
    except ReturnSignal as r:
        return r.value
    finally:
        stack.pop()
        stack_trace.pop()

def eval_expr(node) -> None | int | bool | Any:
    #print('evalExpr de ',node)

    if isinstance(node, NameNode):
        return stack.get_var_value(node.value,stack_trace.copy())

    if isinstance(node, RefNode):
        if stack.get_var_value(node.name,stack_trace.copy()):
            return Reference(node.name)

    if isinstance(node,GroupNode):
        return eval_expr(node.name)

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
                raise TypeException(f"unsupported operand type(s) for {op} : '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left + right
        if op == '-':
            if type(left) != type(right):
                raise TypeException(f"unsupported operand type(s) for {op} : '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left - right
        if op == '*':
            if type(left) != type(right):
                raise TypeException(f"unsupported operand type(s) for {op}: '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left * right
        if op == '/':
            if right == 0:
                raise DivisionByZeroException("division by zero",stack_trace.copy())
            if type(left) != type(right):
                raise TypeException(f"unsupported operand type(s) for {op} : '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left // right
        if op == '>':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left > right
        if op == '<':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left < right
        if op == '==':
            return left == right
        if op == '<=':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left <= right
        if op == '>=':
            if type(left) != type(right):
                raise TypeException(f"{op} not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'",stack_trace.copy())
            return left >= right
        if op == '||': return left or right
        if op == '&&': return left and right
        if op == '!=': return left != right
        if op == '%':
            if type(left) != type(right):
                raise TypeException(f"not all arguments converted during string formatting",stack_trace)
            return left % right

    if isinstance(node, NumberNode):
        return node.number

    if isinstance(node, PointerNode):
        ref = stack.top().get_local_var_value(node.name)

        if not isinstance(ref, Reference):
            raise AttributeException(f"Cannot dereference non-pointer '{type(ref).__name__}'", stack_trace.copy())

        name = ref.value

        try:
            return stack.get_var_value_in_parents(name, stack_trace.copy())
        except NameException:
            pass
        return stack.frames[0].locals[name]

    if isinstance(node, CallNode):
        return eval_call(node)
    return None
