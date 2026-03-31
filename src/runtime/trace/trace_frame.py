from ast_lang.node.bool_node import BoolNode
from ast_lang.node.float_node import FloatNode
from ast_lang.node.name_node import NameNode
from ast_lang.node.number_node import NumberNode
from ast_lang.node.string_node import StringNode


class TraceFrame:
    def __init__(self,func_name,args,line):
        self.func_name = func_name
        self.args = args
        self.line = line

    def format(self):
        list_arg = self.args.args
        for value in list_arg:
            if isinstance(value, NumberNode):
                list_arg = value.number

            if isinstance(value, StringNode):
                list_arg = value.string

            if isinstance(value, FloatNode):
                list_arg = value.number

            if isinstance(value, BoolNode):
                list_arg = value.value

            if isinstance(value,NameNode):
                list_arg = value.value
        return f"in {self.func_name}({""  if list_arg == [] else list_arg }) at {self.line}\n"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(func_name={self.func_name}, args={self.args})"

