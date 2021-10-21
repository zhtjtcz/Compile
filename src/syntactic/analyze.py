from lexical.laxer import tokens
import syntactic.yacc as yacc

def p_CompUnit(p):
	'''
	CompUnit : FuncDef
	'''
	p[0] = p[1]

def p_Funcdef(p):
	'''
	FuncDef : FuncType Ident LPar RPar Block
	'''
	p[0] = [p[1], p[2], p[3], p[4], p[5]]

def p_FuncType(p):
	'''
	FuncType : Int
	'''
	p[0] = p[1]

def p_Ident(p):
	'''
	Ident : Main
	'''
	p[0] = p[1]

def p_Block(p):
	'''
	Block : LBrace Stmt RBrace
	'''
	p[0] = [p[1], p[2], p[3]]

def p_Stmt(p):
	'''
	Stmt : Return Exp Semicolon
	'''
	p[0] = [p[1], p[2], p[3]]

def p_Exp(p):
	'''
	Exp : AddExp
	'''
	p[0] = p[1]

def p_Addexp(p):
	'''
	AddExp : MulExp 
           | AddExp Plus MulExp
		   | AddExp Minus MulExp
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = ' '.join(p[1:])

def p_MulExp(p):
	'''
	MulExp : UnaryExp
           | MulExp Times UnaryExp
		   | MulExp Div UnaryExp
		   | MulExp Mod UnaryExp
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = ' '.join(p[1:])
	
def p_UnaryExp(p):
	'''
	UnaryExp : PrimaryExp
			 | UnaryOp UnaryExp
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = ' '.join(p[1:])

def p_PrimaryExp(p):
	'''
	PrimaryExp : LPar Exp RPar
			   | Number
	'''
	if len(p) == 2:
		p[0] = str(p[1])
	else:
		p[0] = ' '.join(p[1:])

def p_UnaryOp(p):
	'''
	UnaryOp : Plus
			| Minus
	'''
	p[0] = p[1]

def p_erroe(p):
	exit(1)

def getAnalyzer(input, lexer):
	parser = yacc.yacc(start = 'CompUnit')
	result = parser.parse(input, lexer)
	return result