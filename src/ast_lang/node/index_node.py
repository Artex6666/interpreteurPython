<<<<<<< HEAD
from ast_lang.ast_node import AstNode


class IndexNode(AstNode):
    def __init__(self, container, index):
        super().__init__("IndexNode", [container, index])
        self.container = container
        self.index = index

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(container={self.container}, index={self.index})"
=======
from ast_lang.ast_node import AstNode


class IndexNode(AstNode):
    def __init__(self, container, index):
        super().__init__("IndexNode", [container, index])
        self.container = container
        self.index = index

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(container={self.container}, index={self.index})"
>>>>>>> f1e2a59 (no comment)
