from runtime.exception.value_exception import ValueException


class CalcArray:
    def __init__(self, items):
        self.items = list(items)

    def get(self, index, stack_trace):
        if index < 0 or index >= len(self.items):
            raise ValueException(f"array index out of range: {index}", stack_trace.copy())
        return self.items[index]

    def set(self, index, value, stack_trace):
        if index < 0 or index >= len(self.items):
            raise ValueException(f"array index out of range: {index}", stack_trace.copy())
        self.items[index] = value

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self.items) + "]"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(items={self.items})"
