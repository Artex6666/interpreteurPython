class CalcBool:
    def __init__(self, value):
        self.value = bool(value)

    def __str__(self):
        return "true" if self.value else "false"

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.value})"