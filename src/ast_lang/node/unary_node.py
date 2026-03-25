from ast_lang.ast_node import AstNode


class UnaryNode(AstNode):
    def __init__(self,op,right):
        super().__init__("UnaryNode",[right])
        self.op = op
        self.right = right

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(op=\'{self.op}\', right={self.right})"
