from ast_lang.ast_node import AstNode


class ExpressionNode(AstNode):
    def __init__(self,expr):
        super().__init__("ExpressionNode",[expr])
        self.expr = expr
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(expr={self.expr})"