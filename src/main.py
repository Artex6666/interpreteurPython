# -*- coding: utf-8 -*-
from grammar.lexer import lexer
from grammar.parser import parser
from runtime.runtime import eval_inst, stack
from runtime.runtime import functions

source = open("program.cht").read()

ast = parser.parse(source, lexer=lexer)

eval_inst(ast)
print(stack)