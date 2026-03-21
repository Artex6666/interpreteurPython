from ast_lang.ast_node import AstNode


class AssignNode(AstNode):
    def __init__(self, name, expr):
        super().__init__("AssignNode",[expr])
        self.name = name
        self.expr = expr
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name},expr={self.expr})"