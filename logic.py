class ReturnException(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


class ExecutionOutput:
    def __init__(self):
        self.lines = []

    def write(self, text):
        self.lines.append(text)


CURRENT_OUTPUT = None


def emit(text):
    if CURRENT_OUTPUT is not None:
        CURRENT_OUTPUT.write(text)
    print(text)


class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        emit(f"Undefined variable '{name}'")
        return 0

    def set(self, name, value):
        self.vars[name] = value


def eval_program(ast, output=None):
    """Évalue un programme complet (AST racine)."""
    global CURRENT_OUTPUT
    if output is None:
        output = ExecutionOutput()
    CURRENT_OUTPUT = output

    env = Environment()
    functions = {}
    exec_stmt(ast, env, functions)
    return output


def exec_stmt(node, env, functions):
    if not isinstance(node, tuple):
        return

    tag = node[0]

    if tag == 'bloc':
        exec_stmt(node[1], env, functions)
        exec_stmt(node[2], env, functions)

    elif tag == 'assign':
        name = node[1]
        value = eval_expr(node[2], env, functions)
        env.set(name, value)

    elif tag == 'print':
        value = eval_expr(node[1], env, functions)
        emit(f"calc > {value}")

    elif tag == 'if':
        cond = eval_expr(node[1], env, functions)
        if cond:
            exec_stmt(node[2], env, functions)

    elif tag == 'if_else':
        cond = eval_expr(node[1], env, functions)
        if cond:
            exec_stmt(node[2], env, functions)
        else:
            exec_stmt(node[3], env, functions)

    elif tag == 'while':
        while eval_expr(node[1], env, functions):
            exec_stmt(node[2], env, functions)

    elif tag == 'for':
        # ('for', var_name, start_expr, end_expr, body)
        var_name = node[1]
        start = eval_expr(node[2], env, functions)
        end = eval_expr(node[3], env, functions)
        env.set(var_name, start)
        while env.get(var_name) <= end:
            exec_stmt(node[4], env, functions)
            env.set(var_name, env.get(var_name) + 1)

    elif tag == 'empty':
        return

    # Déclaration de fonctions
    elif tag == 'func_def_void':
        # ('func_def_void', nom, [params], corps)
        name, params, body = node[1], node[2], node[3]
        functions[name] = ('void', params, body)

    elif tag == 'func_def_value':
        # ('func_def_value', nom, [params], corps)
        name, params, body = node[1], node[2], node[3]
        functions[name] = ('value', params, body)

    elif tag == 'return':
        value = eval_expr(node[1], env, functions)
        raise ReturnException(value)

    elif tag == 'call':
        # Appel utilisé comme instruction (void ou value, mais on ignore le retour)
        _ = call_function(node[1], node[2], env, functions)


def eval_expr(node, env, functions):
    if isinstance(node, tuple):
        tag = node[0]

        if tag == '+':
            return eval_expr(node[1], env, functions) + eval_expr(node[2], env, functions)
        if tag == '-':
            return eval_expr(node[1], env, functions) - eval_expr(node[2], env, functions)
        if tag == '*':
            return eval_expr(node[1], env, functions) * eval_expr(node[2], env, functions)
        if tag == '/':
            return eval_expr(node[1], env, functions) / eval_expr(node[2], env, functions)
        if tag == '<':
            return eval_expr(node[1], env, functions) < eval_expr(node[2], env, functions)
        if tag == '==':
            return eval_expr(node[1], env, functions) == eval_expr(node[2], env, functions)
        if tag == 'call':
            return call_function(node[1], node[2], env, functions)

        # Si jamais on reçoit un noeud d'instruction en expression (cas étrange)
        exec_stmt(node, env, functions)
        return 0

    if isinstance(node, str):
        return env.get(node)

    # Nombres
    return node


def call_function(name, arg_nodes, env, functions):
    if name not in functions:
        emit(f"Undefined function '{name}'")
        return 0

    func_type, params, body = functions[name]
    if len(params) != len(arg_nodes):
        emit(f"Bad arity in call to '{name}'")
        return 0

    # Environnement local avec liaison des paramètres
    local_env = Environment(parent=env)
    for param, arg_node in zip(params, arg_nodes):
        local_env.set(param, eval_expr(arg_node, env, functions))

    try:
        exec_stmt(body, local_env, functions)
        # Pas de return explicite
        if func_type == 'value':
            # Retour implicite : variable portant le nom de la fonction
            return local_env.get(name)
        return None
    except ReturnException as r:
        # Retour explicite
        if func_type == 'value':
            return r.value
        # fonction void : on ignore la valeur
        return None

