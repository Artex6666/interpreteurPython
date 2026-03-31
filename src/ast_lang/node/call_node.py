from ast_lang.ast_node import AstNode


class CallNode(AstNode):
    def __init__(self,func_name,args,line):
        super().__init__("CallNode",[func_name,args])
        self.func_name = func_name
        self.args = args
        self.line = line
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.func_name}, args={self.args}, line={self.line})"