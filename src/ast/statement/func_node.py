from ast.ast_node import AstNode


class FuncNode(AstNode):
    def __init__(self,func_name,params,bloc):
        super().__init__("FuncNode",[params,bloc])
        self.func_name = func_name
        self.params = params
        self.bloc = bloc
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.func_name}, params={self.params}, bloc={self.bloc})"