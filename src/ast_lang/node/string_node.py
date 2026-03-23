from ast_lang.ast_node import AstNode


class StringNode(AstNode):
    def __init__(self,string):
        super().__init__("StringNode")
        self.string = string

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(string={self.string})"