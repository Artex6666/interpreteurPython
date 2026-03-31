from runtime.trace.stack_trace import StackTrace


class RuntimeException(Exception):
    def __init__(self,message,stack_trace):
        super().__init__(message)
        self.message = message
        self.stack_trace =  stack_trace

    def __str__(self):
        class_name = type(self).__name__
        return f"{class_name}: {self.message}"