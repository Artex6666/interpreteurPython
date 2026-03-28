# -*- coding: utf-8 -*-
from grammar.lexer import lexer
from grammar.parser import parser
from runtime.runtime import eval_inst
from runtime.runtime_exception import RuntimeException
import sys

sys.tracebacklimit = 0

source = open("program.cht").read()

ast = parser.parse(source, lexer=lexer)
try:
    eval_inst(ast)
except RuntimeException as e:
    print(e)