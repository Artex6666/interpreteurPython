# -*- coding: utf-8 -*-
import sys

from grammar.lexer import lexer

sys.tracebacklimit = 0


from runtime.repl import repl


if __name__ == "__main__":
    repl()


