from grammar.lexer import lexer
from grammar.parser import parser
from runtime.runtime import eval_inst
from runtime.runtime_exception import RuntimeException


def run_file(path):
    source = open(path).read()

    ast = parser.parse(source, lexer=lexer)
    try:
        eval_inst(ast)
    except RuntimeException as e:
        print("CALC> " + str(e))
        print(e.stack_trace.format())