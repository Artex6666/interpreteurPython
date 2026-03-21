
class Frame:
    def __init__(self,func_name,func_def,args):
        self.__func_name__ = func_name
        self.__func_def__ = func_def
        self.args = args
        self.frame = {
            "__func_name__": func_name,
            "__func_def__": func_def,
            "args" : args
        }

    def get_frame(self) -> dict:
        return self.frame
