from ast_lang.ast_node import AstNode


class BoolNode(AstNode):
    def __init__(self,value):
        super().__init__("BoolNode",[])
        self.value = value


    def __str__(self):
        return str(self.value).lower()


    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(valeur={self.name})"