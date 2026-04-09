from ast_lang.ast_node import AstNode

class IndexAssignNode(AstNode):
    def __init__(self, name, index, value):
        super().__init__("IndexAssignNode", [index, value])
        self.name = name
        self.index = index
        self.value = value

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name}, index={self.index}, value={self.value})"
