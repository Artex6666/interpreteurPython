class AstNode:
    def __init__(self,name,children=None):
        self.name = name
        self.children = children or []

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name}, children={self.children})"
        