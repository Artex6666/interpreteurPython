from ast_lang.ast_node import AstNode


class ElifNode(AstNode):
    def __init__(self,condition,block):
        super().__init__("ElifNode",[block])
        self.condition = condition
        self.block = block

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(condition={self.condition}, block={self.block})"