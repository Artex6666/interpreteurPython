class StackTrace:
    def __init__(self):
        self.stack_trace = []

    def push(self,frame):
        self.stack_trace.append(frame)

    def pop(self):
        self.stack_trace.pop()

    def format(self):
        result = ""
        for frame in self.stack_trace:
            result += " " + frame.format()
        return  result

    def copy(self):
        new_stack = StackTrace()
        new_stack.stack_trace = self.stack_trace.copy()
        return new_stack
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(stack={self.stack_trace})"