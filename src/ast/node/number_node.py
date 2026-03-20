
from ast.ast_node import AstNode


class NumberNode(AstNode):
    def __init__(self,number):
        super().__init__("NumberNode")
        self.number = number
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(number={self.number})"