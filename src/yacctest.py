from test import tokens,lexer
import syntactic.yacc as yacc

def p_A(p):
	'''	A : A RBrace
	  	  | LBrace
	'''
	if len(p)>=3:
		p[0] = [[p[1],p.lineno(1)], [p[2], p.lineno(2)]]
	else:
		p[0] = p[1]

def p_error(p):
    print('!!')

parser = yacc.yacc(start = 'A')

s = "{}}}}"
result = parser.parse(s, lexer)
print(result)
