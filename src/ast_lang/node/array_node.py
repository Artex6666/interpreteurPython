<<<<<<< HEAD
from ast_lang.ast_node import AstNode


class ArrayNode(AstNode):
    def __init__(self, elements):
        super().__init__("ArrayNode", elements)
        self.elements = elements

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(elements={self.elements})"
=======
from ast_lang.ast_node import AstNode


class ArrayNode(AstNode):
    def __init__(self, elements):
        super().__init__("ArrayNode", elements)
        self.elements = elements

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(elements={self.elements})"
>>>>>>> f1e2a59 (no comment)
