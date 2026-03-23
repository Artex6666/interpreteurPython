from ast_lang.ast_node import AstNode


class IfNode(AstNode):
    def __init__(self,condition,block,elif_list,else_block):
        super().__init__("IfNode",[block])
        self.condition = condition
        self.block = block
        self.elif_list = elif_list or []
        self.else_block = else_block or []

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(conditon={self.condition}, block={self.block}, elif_list={self.elif_list}, else_block={self.block})"