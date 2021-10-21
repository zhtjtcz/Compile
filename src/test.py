import ply.lex as lex

tokens = [
	'NUMBER', 'LPar', 'RPar',
	'LBrace', 'RBrace', 'Semicolon'
]

t_LPar  = r'\('
t_RPar  = r'\)'
t_LBrace = r'\{'
t_RBrace = r'\}'
t_Semicolon = r'\;'
t_ignore  = ' \t'

def t_NUMBER(t):
	r'0[xX][0-9a-fA-F]+|[0-9][0-9]+'
	if t.value[0] == '0' and len(t.value)>1 and t.value[1] not in ['x', 'X']:
		t.value = '0o' + t.value[1:]
	try:
		t.value = eval(t.value)
	except:
		exit(1)
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()
'''
data = "(0010)"

lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: break	  # No more input
	print(tok)
'''