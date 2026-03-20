
from ast.ast_node import AstNode


class EmptyNode(AstNode):
    def __init__(self):
        super().__init__("Empty", [])