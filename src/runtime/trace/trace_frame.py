class TraceFrame:
    def __init__(self,func_name,args):
        self.func_name = func_name
        self.args = args

    def format(self):
        return f"at {self.func_name}({""  if self.args.args == [] else self.args.args })\n"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(func_name={self.func_name}, args={self.args})"

