from ast_lang.ast_node import AstNode

class RefNode(AstNode):
    def __init__(self, value):
        super().__init__("RefNode",[value])
        self.value = value

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(value={self.value})"