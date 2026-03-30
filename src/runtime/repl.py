from grammar.lexer import lexer
from grammar.parser import parser
from runtime.runtime import eval_inst
from runtime.runtime_exception import RuntimeException


def repl():
    while True:
        source = input("CALC> ")

        ast = parser.parse(source, lexer=lexer)

        if source == "exit();":
            break

        try:
            eval_inst(ast)
        except RuntimeException as e:
            print("CALC> " + str(e))