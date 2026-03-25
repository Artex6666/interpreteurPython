from ast_lang.ast_node import AstNode


class PointerAssignNode(AstNode):
    def __init__(self,name,value):
        super().__init__("PointerAssignNode",[value])
        self.name = name
        self.value = value

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name}, value={self.value})"