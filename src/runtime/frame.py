from runtime.exception.name_exception import NameException
from runtime.reference import Reference


class Frame:
    def __init__(self,func_name,func_def,args,stack_trace):
        self.__func_name__ = func_name
        self.__func_def__ = func_def
        self.args = args
        self.locals = {}
        self.stack_trace = stack_trace

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(__func_name__={self.__func_name__}, __func_def__={self.__func_def__}, args={self.args}, locals={self.locals})"

    def add_local_var(self, name, value):
        self.locals[name] = value

    def get_local_var_value(self, name):
        if not name in self.locals:
            raise NameException(f"Variable {name} not found in frame {self.__func_name__}",self.stack_trace)
        return self.locals[name]

    def set_local_var_value(self, name, value):
        if name not in self.locals:
            raise NameException(f"Variable {name} not found in frame {self.__func_name__}",self.stack_trace)
        self.locals[name] = value
