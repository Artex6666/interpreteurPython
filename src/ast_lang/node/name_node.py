from ast_lang.ast_node import AstNode

class NameNode(AstNode):
    def __init__(self, name):
        super().__init__("NameNode",[])
        self.value = name

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(value={self.value})"