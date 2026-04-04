class CalcNumber:
    def __init__(self, value):
        self.value = int(value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.value})"