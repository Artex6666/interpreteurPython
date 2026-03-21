
from ast_lang.ast_node import AstNode


class EmptyNode(AstNode):
    def __init__(self):
        super().__init__("Empty", [])
    def __len__(self):
        return 0