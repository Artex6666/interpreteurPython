class Stack:
    def __init__(self):
        self.frames = []

    def push(self, frame):
        self.frames.append(frame)

    def pop(self):
        return self.frames.pop()

    def top(self):
        return self.frames[-1]

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(frames={self.frames})"