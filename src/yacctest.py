from test import tokens,lexer
import ply.yacc as yacc

def p_A(p):
	'''	A : A RBrace
	  	  | LBrace
	'''
	p[0] = ' '.join(p[1:])

def p_error(p):
    print('!!')

parser = yacc.yacc(start = 'A')

s = "{}}}}"
result = parser.parse(s, lexer)
print(result)
