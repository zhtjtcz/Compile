from lexical.laxer import tokens
import syntactic.yacc as yacc

def p_CompUnit(p):
	'''
	CompUnit : Int
	'''
	print(p[1])

def p_erroe(p):
	exit(1)

def getAnalyzer(input, lexer):
	parser = yacc.yacc(start = 'CompUnit')
	result = parser.parse(input, lexer)
	return result