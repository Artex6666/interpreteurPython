from ast_lang.ast_node import AstNode


class FloatNode(AstNode):
    def __init__(self,number):
        super().__init__("FloatNode",[])
        self.number = number

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(number={self.number})"