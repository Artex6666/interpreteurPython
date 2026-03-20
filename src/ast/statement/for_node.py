from ast.ast_node import AstNode


class ForNode(AstNode):
    def __init__(self, init, cond, incr, body):
        super().__init__("ForNode",[init,incr,body])
        self.init = init
        self.cond = cond
        self.incr = incr
        self.body = body

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(init={self.init}, cond={self.cond}, incr={self.incr})"