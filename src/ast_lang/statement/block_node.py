from ast_lang.ast_node import AstNode


class BlocKNode(AstNode):
    def __init__(self,first,second):
        super().__init__("BlockNode",[first,second])
        self.first = first
        self.second = second

    def clone(self):
        return BlocKNode(self.first, self.second)

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(first={self.first},second={self.second})"