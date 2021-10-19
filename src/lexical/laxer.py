from values import *
import lexical.lex as lex
# import ply.lex as lex

reserved = {
	'main': 'Main',
	'int': 'Int',
	'return': 'Return'
}

def t_Number(t):
	r'0[xX][0-9a-fA-F]+|[0-9][0-9]*'
	if t.value[0] == '0' and len(t.value)>1 and t.value[1] not in ['x', 'X']:
		t.value = '0o' + t.value[1:]
	try:
		t.value = eval(t.value)
	except:
		exit(1)
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')	# Check for reserved words
	if t.type == 'ID':
		exit(1)
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	exit(1)

def getTokens(input, outputFile):
	result = []

	tokens = [
		'Number', 'LPar', 'RPar',
		'LBrace', 'RBrace', 'Semicolon', 'ID',
		'Plus', 'Minus', 'Times', 'Div', 'Mod'
	] + list(reserved.values())

	t_LPar  = r'\('
	t_RPar  = r'\)'
	t_LBrace = r'\{'
	t_RBrace = r'\}'
	t_Semicolon = r'\;'
	t_ignore  = ' \t'
	t_Plus = r'\+'
	t_Minus = r'\-'
	t_Times = r'\*'
	t_Div = r'\/'
	t_Mod = r'\%'

	lexer = lex.lex()
	lexer.input(input)
	while True:
		token = lexer.token()
		if not token:
			break	  # No more input
		if LOCAL:
			print(token, file=outputFile)
		result.append(token)
	return result