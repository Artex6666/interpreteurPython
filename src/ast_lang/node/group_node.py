from ast_lang.ast_node import AstNode


class GroupNode(AstNode):
    def __init__(self, name):
        super().__init__("GroupNode",[name])
        self.name = name
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name})"