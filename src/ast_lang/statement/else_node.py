from ast_lang.ast_node import AstNode


class ElseNode(AstNode):
    def __init__(self,block):
        super().__init__("ElseNode")
        self.block = block

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(block={self.block})"