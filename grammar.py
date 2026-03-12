import ply.lex as lex
import ply.yacc as yacc

# Mots réservés
reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'to': 'TO',
    'fonctionVoid': 'FONCTIONVOID',
    'fonctionValue': 'FONCTIONVALUE',
    'return': 'RETURN',
}

# Liste des tokens
tokens = [
    'NUMBER', 'MINUS',
    'PLUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'NAME', 'EQUALS', 'SEMI',
    'LBRACE', 'RBRACE',
    'COMMA',
    'LT', 'EQEQ',
] + list(reserved.values())

# Expressions régulières pour les tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMI = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_LT = r'<'
t_EQEQ = r'=='


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construction du lexer
lexer = lex.lex()

# Précédence des opérateurs
precedence = (
    ('left', 'LT', 'EQEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


# --------- RÈGLES DE GRAMMAIRE (AST) ----------

def p_start(p):
    'start : statement_list'
    p[0] = p[1]


def p_statement_list_one(p):
    'statement_list : statement'
    p[0] = p[1]


def p_statement_list_more(p):
    'statement_list : statement_list SEMI statement'
    p[0] = ('bloc', p[1], p[3])


def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    p[0] = ('assign', p[1], p[3])


def p_statement_block(p):
    'statement : LBRACE statement_list RBRACE'
    p[0] = p[2]


def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print', p[3])


def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN statement'
    p[0] = ('if', p[3], p[5])


def p_statement_if_else(p):
    'statement : IF LPAREN expression RPAREN statement ELSE statement'
    p[0] = ('if_else', p[3], p[5], p[7])


def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN statement'
    p[0] = ('while', p[3], p[5])


def p_statement_for(p):
    'statement : FOR LPAREN NAME EQUALS expression TO expression RPAREN statement'
    p[0] = ('for', p[3], p[5], p[7], p[9])


def p_statement_empty(p):
    'statement : '
    p[0] = ('empty',)


# ----- FONCTIONS -----

def p_statement_func_void(p):
    'statement : FONCTIONVOID NAME LPAREN param_list_opt RPAREN LBRACE statement_list RBRACE'
    # ('func_def_void', nom, [params], corps)
    p[0] = ('func_def_void', p[2], p[4], p[7])


def p_statement_func_value(p):
    'statement : FONCTIONVALUE NAME LPAREN param_list_opt RPAREN LBRACE statement_list RBRACE'
    # ('func_def_value', nom, [params], corps)
    p[0] = ('func_def_value', p[2], p[4], p[7])


def p_param_list_opt_empty(p):
    'param_list_opt : '
    p[0] = []


def p_param_list_opt_nonempty(p):
    'param_list_opt : param_list'
    p[0] = p[1]


def p_param_list_single(p):
    'param_list : NAME'
    p[0] = [p[1]]


def p_param_list_multi(p):
    'param_list : param_list COMMA NAME'
    p[0] = p[1] + [p[3]]


def p_statement_return(p):
    'statement : RETURN expression'
    p[0] = ('return', p[2])


def p_statement_call(p):
    'statement : NAME LPAREN arg_list_opt RPAREN'
    p[0] = ('call', p[1], p[3])


def p_arg_list_opt_empty(p):
    'arg_list_opt : '
    p[0] = []


def p_arg_list_opt_nonempty(p):
    'arg_list_opt : arg_list'
    p[0] = p[1]


def p_arg_list_single(p):
    'arg_list : expression'
    p[0] = [p[1]]


def p_arg_list_multi(p):
    'arg_list : arg_list COMMA expression'
    p[0] = p[1] + [p[3]]


# ----- EXPRESSIONS -----

def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    p[0] = ('+', p[1], p[3])


def p_expression_binop_minus(p):
    'expression : expression MINUS expression'
    p[0] = ('-', p[1], p[3])


def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    p[0] = ('*', p[1], p[3])


def p_expression_binop_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = ('/', p[1], p[3])


def p_expression_lt(p):
    'expression : expression LT expression'
    p[0] = ('<', p[1], p[3])


def p_expression_eqeq(p):
    'expression : expression EQEQ expression'
    p[0] = ('==', p[1], p[3])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]


def p_expression_call(p):
    'expression : NAME LPAREN arg_list_opt RPAREN'
    p[0] = ('call', p[1], p[3])


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


def parse(text):
    """Construit et renvoie l'AST pour le programme donné."""
    return parser.parse(text, lexer=lexer)

