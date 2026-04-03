from runtime.exception.name_exception import NameException
from runtime.runtime_exception import RuntimeException


class Stack:
    def __init__(self):
        self.frames = []

    def push(self, frame):
        self.frames.append(frame)

    def pop(self):
        return self.frames.pop()

    def top(self):
        return self.frames[-1]

    def get_var_value(self, name,stack_trace):
        for frame in reversed(self.frames):
            if name in frame.locals:
                return frame.locals[name]
        raise NameException(f"Variable {name} not found",stack_trace)

    def set_var_value(self, name, value,stack_trace):
        for frame in reversed(self.frames):
            if name in frame.locals:
                frame.locals[name] = value
                return
        raise NameException(f"Variable {name} not found",stack_trace)

    def get_var_value_in_parents(self, name,stack_trace):
        for frame in reversed(self.frames[:-1]):
            if name in frame.locals:
                return frame.locals[name]
        raise NameException(f"Variable {name} not found in parents",stack_trace)

    def set_var_value_in_parents(self, name, value,stack_trace):
        for frame in reversed(self.frames[:-1]):
            if name in frame.locals:
                frame.locals[name] = value
                return
        raise NameException(f"Variable {name} not found in parents",stack_trace)

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(frames={self.frames})"