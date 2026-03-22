
class FuncTable:
    def __init__(self):
        self._table = {}

    def add_func(self,func):
        self._table[func.func_name] = {
            "params": func.params,
            "body": func.body,
            "node": func
        }

    def get(self, name):
        return self._table[name]
