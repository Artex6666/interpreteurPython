from ast.ast_node import AstNode


class PrintNode(AstNode):
    def __init__(self,content):
        super().__init__("PrintNode",[content])
        self.content = content
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(content={self.content})"