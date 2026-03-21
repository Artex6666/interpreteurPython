
class FuncTable:
    def __init__(self):
        self._table = {}
        self._func_info = {
            None :{
                "params" : None,
                "body" : None
            }
        }

    def add_func(self,func) -> dict:
        self._func_info = {
            func.func_name: {
                "params": func.params,
                "body": func.body
            }
        }

        self._table.update(self._func_info)
        return self._table
