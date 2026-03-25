from ast_lang.ast_node import AstNode

class RefNode(AstNode):
    def __init__(self, name):
        super().__init__("RefNode",[])
        self.name = name

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name})"