from ast_lang.ast_node import AstNode


class ParamsNode(AstNode):
    def __init__(self,args):
        super().__init__("ParamsNode",args or [])
        self.args = args

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(args={self.children})"