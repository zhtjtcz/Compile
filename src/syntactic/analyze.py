from lexical.laxer import tokens
import syntactic.yacc as yacc
from syntactic.node import Node
from values import *

def p_CompUnit(p):
	'''
	CompUnit : FuncDef
	'''
	p[0] = Node('CompUnit', children = p[1:])

def p_Decls(p):
	'''
	Decsl : Decl Decls
		  |
	'''
	if len(p) == 1:
		return None
	else:
		p[0] = Node('Decls')
		if p[2] == None:
			p[0].children = [p[1]]
		else:
			p[0].children = [p[1]] + p[2].children[:]

def p_Decl(p):
	'''
	Decl : ConstDecl
		 | VarDecl
	'''
	p[0] = Node('Decl', children = p[1:])

def p_ConstDecl(p):
	'''
	ConstDecl : Const BType ConstDefs Semicolon
	'''
	p[0] = Node('ConstDecl', children = p[3].children)

def p_ConstDefs(p):
	'''
	ConstDefs : ConstDef
			  | ConstDefs Comma ConstDef
	'''
	if len(p) == 2:
		p[0] = Node('ConstDefs', children = [p[1]])
	else:
		p[0] = Node('ConstDefs', children = p[1].children + [p[3]])

def p_BType(p):
	'''
	BType : Int
	'''
	p[0] = Node('Int')
	# Only one type!

def p_ConstDef(p):
	'''
	ConstDef : Ident Equal ConstInitVal
	'''
	p[1] = Node('Ident', name = p[1])
	p[0] = Node('ConstDef', children = [p[1], p[3]])

def p_ConstInitVal(p):
	'''
	ConstInitVal : ConstExp
	'''
	p[0] = Node('ConstInitVal', children = p[1:])

def p_ConstExp(p):
	'''
	ConstExp : AddExp
	'''
	p[0] = Node('ConstExp', children = p[1:])

def p_VarDecl(p):
	'''
	VarDecl : BType VarDefs Semicolon
	'''
	p[0] = Node('VarDecl', children = p[2].children)

def p_Vardefs(p):
	'''
	VarDefs : VarDef
			| VarDefs Comma VarDef
	'''
	if len(p) == 2:
		p[0] = Node('VarDefs', children = [p[1]])
	else:
		p[0] = Node('VarDefs', children = p[1].children + [p[3]])	

def p_VarDef(p):
	'''
	VarDef : Ident Equal InitVal
           | Ident
	'''
	if len(p) == 2:
		x = Node("Ident", name = p[1])
		p[0] = Node("VarDef", children = [x])
	else:
		x = Node("Ident", name = p[1])
		p[0] = Node('VarDef', children = [x, p[3]])

def p_InitVal(p):
	'''
	InitVal : Exp
	'''
	p[0] = Node('InitVal', children = p[1:])

def p_Funcdef(p):
	'''
	FuncDef : FuncType Main LPar RPar Block
	'''
	l = Node('LBrace', name = '(')
	r = Node('RBrace', name = ')')
	x = Node('Ident', name = 'main')
	p[0] = Node('FuncDef', children = [p[1], x, l, r, p[5]])

def p_FuncType(p):
	'''
	FuncType : Int
	'''
	p[0] = Node('FuncType', name = p[1])

def p_Block(p):
	'''
	Block : LBrace BlockItems RBrace
	'''
	p[0] = Node('Block', children = [p[2]])

def p_BlockItems(p):
	'''
	BlockItems :
			   | BlockItems BlockItem
	'''
	if len(p) == 1:
		p[0] = None
	else:
		if p[1] == None:
			p[0] = Node('BlockItems', children = [p[2]])
		else:
			p[0] = Node('BlockItems', children = p[1].children + [p[2]])

def p_BlockItem(p):
	'''
	BlockItem : Decl
			  | Stmt
	'''
	p[0] = p[1]
	# p[0] = Node('BlockItem', children = p[1:])

def p_Stmt(p):
	'''
	Stmt : Semicolon
		 | Block
		 | Exp Semicolon
		 | Return Exp Semicolon
		 | LVal Equal Exp Semicolon
		 | If LPar Cond RPar Stmt Else Stmt
		 | If LPar Cond RPar Stmt
	'''
	if len(p) == 2:
		p[0] = Node('Stmt')
		if p[1].type == 'Block':
			p[0].children = p[1:]
	elif len(p) == 3:
		p[0] = Node('Stmt', children = [p[1]])
	elif len(p) == 4:
		l = Node('Return')
		p[0] = Node('Stmt', children = [l, p[2]])
	elif len(p) == 5:
		l = Node('Equal')
		p[0] = Node('Stmt', children = [p[1], l, p[3]])
	elif len(p)==6:
		l = Node('(')
		r = Node(')')
		p[0] = Node('Stmt', children = [p[3], p[5], l, r])
	elif len(p) == 8:
		l = Node('(')
		r = Node(')')
		p[0] = Node('Stmt', children = [p[3], p[5], p[7], l, r])

def p_LVal(p):
	'''
	LVal : Ident
	'''
	p[0] = Node('LVal', name = p[1])

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
		p[0] = Node('MulExp', children = p[1:])

def p_UnaryExp(p):
	'''
	UnaryExp : PrimaryExp
			 | UnaryOp UnaryExp
			 | Ident LPar RPar
			 | Ident LPar FuncRParams RPar
	'''
	if len(p)<=3:
		p[0] = Node('UnaryExp', children = p[1:])
	elif len(p) == 4:
		x = Node('Ident', name = p[1])
		p[0] = Node('UnaryExp', children = [x, Node('('), Node(')')])
	else:
		x = Node('Ident', name = p[1])
		p[0] = Node('UnaryExp', children = [x, Node('('), p[3], Node(')')])

def p_FuncRParams(p):
	'''
	FuncRParams : Exp
				| Exp Exps
	'''
	if len(p) == 3:
		p[0] = Node('FuncRParams', children = [p[1]] + p[2].children)
	else:
		p[0] = Node('FuncRParams', children = [p[1]])

def p_Exps(p):
	'''
	Exps : Comma Exp
		 | Comma Exp Exps
	'''
	if len(p) == 3:
		p[0] = Node('Exps', children = [p[2]])
	else:
		p[0] = Node('Exps', children = [p[2]] + p[3].children)

def p_PrimaryExp(p):
	'''
	PrimaryExp : LPar Exp RPar
			   | Number
			   | LVal
	'''
	if len(p) == 2:
		if str(p[1]).isdigit():
			x = Node('Number', value = int(p[1]))
			p[0] = Node('PrimaryExp', children = [x])
		else:
			x = Node('LVal', name = p[1].name)
			p[0] = Node('PrimaryExp', children = [x])
	else:
		p[0] = Node('PrimaryExp', children = [Node('('), p[2], Node(')')])

def p_UnaryOp(p):
	'''
	UnaryOp : Plus
			| Minus
			| Not
	'''
	p[0] = Node(p[1])

def p_Cond(p):
	'''
	Cond : LOrExp
	'''
	p[0] = Node('Cond', children = [p[1]])

def p_LOrExp(p):
	'''
	LOrExp : LAndExp
           | LOrExp Or LAndExp
	'''
	if len(p) == 2:
		p[0] = Node('LOrExp', children = [p[1]])
	else:
		p[0] = Node('LOrExp', children = [p[1], p[3]])

def p_LAndExp(p):
	'''
	LAndExp : EqExp
            | LAndExp And EqExp
	'''
	if len(p) == 2:
		p[0] = Node('LAndExp', children = [p[1]])
	else:
		p[0] = Node('LAndExp', children = [p[1], p[3]])

def p_EqExp(p):
	'''
	EqExp : RelExp
    	  | EqExp Deq RelExp
		  | EqExp Neq RelExp
	'''
	if len(p) == 2:
		p[0] = Node('EqExp', children = p[1:])
	else:
		op = Node(p[2])
		p[0] = Node('EqExp', children = [p[1], op, p[3]])

def p_RelExp(p):
	'''
	RelExp : AddExp
    	   | RelExp Less AddExp
		   | RelExp More AddExp
		   | RelExp Leq AddExp
		   | RelExp Geq AddExp
	'''
	if len(p) == 2:
		p[0] = Node('RelExp', children = [p[1]])
	else:
		op = Node(p[2])
		p[0] = Node('RelExp', children = [p[1], op, p[3]])

def p_error(p):
	print(p)
	exit(1)

def getAnalyzer(input, lexer):
	parser = yacc.yacc(start = 'CompUnit')
	result = parser.parse(input, lexer)
	return result
