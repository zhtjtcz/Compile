from lexical.laxer import tokens
import syntactic.yacc as yacc
from syntactic.node import Node
from values import *

def p_CompUnit(p):
	'''
	CompUnit : Definelist
	'''
	p[0] = p[0] = Node('CompUnit', children = p[1:])

def p_Definelist(p):
	'''
	Definelist : Definelist Define
			   | Define
	'''
	if len(p) == 2:
		p[0] = Node('Definelist', children = [p[1]])
	else:
		p[0] = Node('Definelist', children = p[1].children + [p[2]])

def p_Define(p):
	'''
	Define : Decl
		   | FuncDef
	'''
	p[0] = Node('Define', children = [p[1]])

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
			  | ConstDef Comma ConstDefs
	'''
	if len(p) == 2:
		p[0] = Node('ConstDefs', children = [p[1]])
	else:
		p[0] = Node('ConstDefs', children = [p[1]] + p[3].children)

def p_BType(p):
	'''
	BType : Int
		  | Void
	'''
	if p[1] == 'int':
		p[0] = Node('Int')
	elif p[1] == 'void':
		p[0] = Node('Void')
	# Only one type!

def p_ConstDef(p):
	'''
	ConstDef : Ident Equal ConstInitVal
			 | Ident ConstSubs Equal ConstInitVal
	'''
	if len(p) == 4:
		p[0] = Node('ConstDef', children = [Node('Ident', name = p[1]), p[3]])
	else:
		p[0] = Node('ConstDef', children = [Node('Ident', name = p[1]), p[2], p[4]])

def p_ConstSubs(p):
	'''
	ConstSubs : ConstSub ConstSubs
			  | ConstSub
	'''
	if len(p) == 2:
		p[0] = Node('ConstSubs', children = [p[1].children[0]])
	else:
		p[0] = Node('ConstSubs', children = [p[1].children[0]] + p[2].children)

def p_ConstSub(p):
	'''
	ConstSub : LSPar ConstExp RSPar
	'''
	p[0] = Node('ConstSub', children = [p[2].children[0]])

def p_ConstInitVal(p):
	'''
	ConstInitVal : ConstExp
				 | LBrace RBrace
				 | LBrace ConstInitVal RBrace
				 | LBrace ConstInitVal ConstInitVals RBrace
	'''
	if len(p) == 2:
		p[0] = Node('ConstInitVal', children = p[1:])
	elif len(p) == 3:
		p[0] = Node('ConstInitVal')
	elif len(p) == 4:
		p[0] = Node('ConstInitVal', children = [Node('{'), p[2], Node('}')])
	else:
		p[0] = Node('ConstInitVal', children = [Node('{'), p[2]] + p[3].children + [Node('}')])

def p_ConstInitVals(p):
	'''
	ConstInitVals : Comma ConstInitVal
				  | Comma ConstInitVal ConstInitVals
	'''
	if len(p) == 3:
		p[0] = Node('ConstInitVals', children = [p[2]])
	else:
		p[0] = Node('ConstInitVals', children = [p[2]] + p[3].children)

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
	VarDef : Ident
		   | Ident ConstSubs
           | Ident Equal InitVal
		   | Ident ConstSubs Equal InitVal
	'''
	x = Node("Ident", name = p[1])
	if len(p) == 2:
		p[0] = Node("VarDef", children = [x])
	elif len(p) == 3:
		p[0] = Node('VarDef', children = [x, p[2]])
	elif len(p) == 4:
		p[0] = Node('VarDef', children = [x, p[3]])
	else:
		p[0] = Node('VarDef', children = [x, p[2], p[4]])

def p_InitVals(p):
	'''
	InitVals : Comma InitVal
			 | Comma InitVal InitVals
	'''
	if len(p) == 3:
		p[0] = Node('InitVals', children = [p[2]])
	else:
		p[0] = Node('InitVals', children = [p[2]] + p[3].children)

def p_InitVal(p):
	'''
	InitVal : Exp
			| LBrace RBrace
			| LBrace InitVal RBrace
			| LBrace InitVal InitVals RBrace
	'''
	if len(p) == 2:
		p[0] = Node('InitVal', children = p[1:])
	elif len(p) == 3:
		p[0] = Node('InitVal')
	elif len(p) == 4:
		p[0] = Node('InitVal', children = [Node('{'), p[2], Node('}')])
	else:
		p[0] = Node('InitVal', children = [Node('{'), p[2]] + p[3].children + [Node('}')])

def p_Funcdef(p):
	'''
	FuncDef : BType Ident LPar RPar Block
	        | BType Ident LPar FuncFParams RPar Block
	'''
	x = Node('Ident', name = p[2])
	if len(p) == 6:
		p[0] = Node('FuncDef', children = [p[1], x, p[5]])
	else:
		p[0] = Node('FuncDef', children = [p[1], x, p[4], p[6]])

def p_FuncFParams(p):
	'''
	FuncFParams : FuncFParam
				| FuncFParam Comma FuncFParams
	'''
	if len(p) == 2:
		p[0] = Node('FuncFParams', children = [p[1]])
	else:
		p[0] = Node('FuncFParams', children = [p[1]] + p[3].children)

def p_FuncFParam(p):
	'''
	FuncFParam : BType Ident
			   | BType Ident LSPar RSPar
			   | BType Ident LSPar RSPar ParParams
	'''
	p[0] = Node('FuncFParam', p[1:])

def p_ParParams(p):
	'''
	ParParams : LSPar Exp RSPar
			  | LSPar Exp RSPar ParParams
	'''
	if len(p) == 4:
		p[0] = Node('ParParams', children = [p[2]])
	else:
		p[0] = Node('ParParams', children = [p[2]] + p[4].children)

def p_Block(p):
	'''
	Block : LBrace BlockItems RBrace
	'''
	p[0] = Node('Block')
	if p[2] != None:
		p[0].children = [p[2]]

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

def p_Stmt(p):
	'''
	Stmt : Semicolon
		 | Block
		 | Break
		 | Continue
		 | Exp Semicolon
		 | Return Semicolon
		 | Return Exp Semicolon
		 | LVal Equal Exp Semicolon
		 | While LPar Cond RPar Stmt
		 | If LPar Cond RPar Stmt Else Stmt
		 | If LPar Cond RPar Stmt
	'''
	if len(p) == 2:
		p[0] = Node('Stmt')
		if p[1] == 'break' or p[1] == 'continue':
			p[0].children = [Node(p[1])]
		elif p[1] == ';':
			return
		elif p[1].type == 'Block':
			p[0].children = p[1:]
	elif len(p) == 3:
		p[0] = Node('Stmt', children = [p[1]])
	elif len(p) == 4:
		p[0] = Node('Stmt', children = [Node('Return'), p[2]])
	elif len(p) == 5:
		p[0] = Node('Stmt', children = [p[1], Node('Equal'), p[3]])
	elif len(p)==6:
		if p[1] == 'while':
			p[0] = Node('Stmt', children = [p[3], p[5]])
		else:
			p[0] = Node('Stmt', children = [p[3], p[5], Node('('), Node(')')])
	elif len(p) == 8:
		p[0] = Node('Stmt', children = [p[3], p[5], p[7], Node('('), Node(')')])

def p_LVal(p):
	'''
	LVal : Ident ConstSubs
		 | Ident
	'''
	if len(p) == 2:
		p[0] = Node('LVal', name = p[1])
	else:
		p[0] = Node('LVal', name = p[1], children = [p[2]])

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
		p[0] = Node('AddExp', children = [p[1], Node(p[2]), p[3]])
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
		p[0] = Node('MulExp', children = [p[1], Node(p[2]), p[3]])
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
			x = Node('LVal', name = p[1].name, children = p[1].children)
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
		p[0] = Node('EqExp', children = [p[1], Node(p[2]), p[3]])

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
		p[0] = Node('RelExp', children = [p[1], Node(p[2]), p[3]])

def p_error(p):
	print(p)
	exit(1)

def getAnalyzer(input, lexer):
	parser = yacc.yacc(start = 'CompUnit')
	result = parser.parse(input, lexer)
	return result
