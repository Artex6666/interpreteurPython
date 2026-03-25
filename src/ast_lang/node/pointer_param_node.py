from ast_lang.ast_node import AstNode


class PointerParamNode(AstNode):
    def __init__(self,name):
        super().__init__("PointerParam",[])
        self.name = name

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name})"