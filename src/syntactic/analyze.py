from lexical.laxer import tokens
import syntactic.yacc as yacc
from syntactic.node import Node

def p_CompUnit(p):
	'''
	CompUnit : FuncDef
	'''
	p[0] = Node('CompUnit', children = p[1:])

def p_Funcdef(p):
	'''
	FuncDef : FuncType Ident LPar RPar Block
	'''
	p[0] = Node('FuncDef', children = p[1:])

def p_FuncType(p):
	'''
	FuncType : Int
	'''
	p[0] = Node('FuncType', children = p[1:])

def p_Ident(p):
	'''
	Ident : Main
	'''
	p[0] = Node('Ident', children = p[1:])

def p_Block(p):
	'''
	Block : LBrace Stmt RBrace
	'''
	p[0] = Node('Block', children = p[1:])

def p_Stmt(p):
	'''
	Stmt : Return Exp Semicolon
	'''
	p[0] = Node('Stmt', children = p[1:])

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
	p[0] = Node('AddExp', children = p[1:])

def p_MulExp(p):
	'''
	MulExp : UnaryExp
           | MulExp Times UnaryExp
		   | MulExp Div UnaryExp
		   | MulExp Mod UnaryExp
	'''
	p[0] = Node('MulExp', children = p[1:])

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
	p[0] = Node('PrimaryExp', children = p[1:]) 

def p_UnaryOp(p):
	'''
	UnaryOp : Plus
			| Minus
	'''
	p[0] = Node('UnaryOp', name = p[1])

def p_erroe(p):
	exit(1)

def getAnalyzer(input, lexer):
	parser = yacc.yacc(start = 'CompUnit')
	result = parser.parse(input, lexer)
	return result