class Reference:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(value={self.value})"