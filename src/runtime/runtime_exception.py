class RuntimeException(Exception):
    def __init__(self,message):
        super().__init__(message)
        self.message = message
    def __str__(self):
        class_name = type(self).__name__
        return f"{class_name}: {self.message}"