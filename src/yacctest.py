from test import tokens
import ply.yacc as yacc

def p_a(p):
	'''
	a : a RBrace
				| LBrace
	'''
	if len(p) != 1:
		p[0] = p[1] + '}'
	else:
		p[0] = '{'

def p_error(p):
    print('!!')

parser = yacc.yacc()

s = "{}}}}"
result = parser.parse(s)
print(result)
