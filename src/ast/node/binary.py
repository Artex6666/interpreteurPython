from ast.ast_node import AstNode


class BinaryNode(AstNode):
    def __init__(self, op:str, left, right):
        super().__init__(f"BinaryOp({op})",[left,right])
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(operator={self.op}, left_operand={self.left}, right_operand={self.right})"