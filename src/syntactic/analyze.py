from lexical.laxer import tokens
import syntactic.yacc as yacc
from syntactic.node import Node
from values import *
from syntactic.table import table

def p_CompUnit(p):
	'''
	CompUnit : FuncDef
	'''
	p[0] = Node('CompUnit', children = p[1:])

def p_Funcdef(p):
	'''
	FuncDef : FuncType Ident LPar RPar Block
	'''
	l = Node('LBrace', name = '(')
	r = Node('RBrace', name = ')')
	p[0] = Node('FuncDef', children = [p[1], p[2], l, r, p[5]])

def p_FuncType(p):
	'''
	FuncType : Int
	'''
	p[0] = Node('FuncType', name = p[1])

def p_Ident(p):
	'''
	Ident : Main
	'''
	p[0] = Node('Ident', name = p[1])

def p_Block(p):
	'''
	Block : LBrace Stmt RBrace
	'''
	l = Node('LBrace', name = '(')
	r = Node('RBrace', name = ')')
	p[0] = Node('Block', children = [l, p[2], r])

def p_Stmt(p):
	'''
	Stmt : Return Exp Semicolon
	'''
	l = Node('Return')
	r = Node('Semicolon')
	p[0] = Node('Stmt', children = [l, p[2], r])

def p_Exp(p):
	'''
	Exp : AddExp
	'''
	p[0] = Node('Exp', children = p[1:])

def p_Addexp(p):
	'''
	AddExp : MulExp 
           | AddExp Plus MulExp
		   | AddExp Minus MulExp
	'''

	if len(p) > 2:
		op = Node(p[2])
		p[0] = Node('AddExp', children = [p[1], op, p[3]])
	else:
		p[0] = Node('AddExp', children = p[1:])

def p_MulExp(p):
	'''
	MulExp : UnaryExp
           | MulExp Times UnaryExp
		   | MulExp Div UnaryExp
		   | MulExp Mod UnaryExp
	'''
	if len(p) > 2:
		op = Node(p[2])
		p[0] = Node('MulExp', children = [p[1], op, p[3]])
	else:
		p[0] = Node('MulExp', children =p[1:])

def p_UnaryExp(p):
	'''
	UnaryExp : PrimaryExp
			 | UnaryOp UnaryExp
	'''
	p[0] = Node('UnaryExp', children = p[1:])

def p_PrimaryExp(p):
	'''
	PrimaryExp : LPar Exp RPar
			   | Number
	'''
	if len(p) == 2:
		p[0] = Node('Number', value = int(p[1]))
	else:
		l = Node('LBrace', name = '(')
		r = Node('RBrace', name = ')')
		p[0] = Node('PrimaryExp', children = [l, p[2], r])

def p_UnaryOp(p):
	'''
	UnaryOp : Plus
			| Minus
	'''
	p[0] = Node(p[1])

def p_erroe(p):
	exit(1)

def getAnalyzer(input, lexer):
	parser = yacc.yacc(start = 'CompUnit')
	result = parser.parse(input, lexer)
	return result

def dfs(x : Node):
	if x.type == 'CompUnit':
		dfs(x.children[0])
	elif x.type == 'FuncDef':
		print('define dso_local i32 @main()', file = outputFile, end = '')
		dfs(x.children[-1])
	elif x.type == 'Block':
		print('{', file = outputFile)
		dfs(x.children[1])
		print('}', file = outputFile)
	elif x.type == 'Stmt':
		dfs(x.children[1])
		print('ret i32', file = outputFile, end = ' ')
		print(x.children[1].name, file = outputFile)
	elif x.type == 'Exp':
		dfs(x.children[0])
		x.name = x.children[0].name
	elif x.type == 'AddExp':
		if len(x.children) == 1:
			dfs(x.children[0])
			x.name = x.children[0].name
		else:
			dfs(x.children[2])
			dfs(x.children[0])
			x.name = table.create_val()
			if x.children[1].type == '+':
				print(x.name, '= add', x.children[0].name,  x.children[2].name, file = outputFile)
			else:
				print(x.name, '= sub', x.children[0].name,  x.children[2].name, file = outputFile)
	elif x.type == 'MulExp':
		if len(x.children) == 1:
			dfs(x.children[0])
			x.name = x.children[0].name
		else:
			dfs(x.children[2])
			dfs(x.children[0])
			x.name = table.create_val()
			if x.children[1].type == '*':
				print(x.name, '= mul', x.children[0].name,  x.children[2].name, file = outputFile)
			elif x.children[1].type == '/':
				print(x.name, '= sdiv', x.children[0].name,  x.children[2].name, file = outputFile)
			else:
				print(x.name, '= srem', x.children[0].name,  x.children[2].name, file = outputFile)
	elif x.type == 'UnaryExp':
		if len(x.children) == 1:
			dfs(x.children[0])
			x.name = x.children[0].name
		else:
			dfs(x.children[1])
			x.name = table.create_val()
			if x.children[0].type == '+':
				print(x.name, '= add i32 0', x.children[1].name, file = outputFile)
			else:
				print(x.name, '= sub i32 0', x.children[1].name, file = outputFile)
	elif x.type == 'PrimaryExp':
		if len(x.children) == 1:
			x.name = str(x.children[0].value)
		else:
			dfs(x.children[1])
			x.name = x.children[1].name
	elif x.type == 'Number':
		x.name = str(x.value)
