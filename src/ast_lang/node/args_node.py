from ast_lang.ast_node import AstNode


class ArgsNode(AstNode):
    def __init__(self,args):
        super().__init__("ArgsNode",args or [])
        self.args = args
        self.len = args.__len__()

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(args={self.children})"