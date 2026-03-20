from ast.ast_node import AstNode


class WhileNode(AstNode):
    def __init__(self, condition, block):
        super().__init__("WhileNode",[block])
        self.condition = condition
        self.block = block
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(conditon={self.condition}, block={self.block})"