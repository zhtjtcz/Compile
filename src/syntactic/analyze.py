from values import *

class Analyzer:
	def __init__(self, tokens, outputfile):
		self.tokens = tokens[::-1]
		self.token = None
		self.last = None
		self.outputfile = outputfile
	
	def Ready(self):
		print("Analyzer Ready!")
		print("total %d tokens"%(len(self.tokens)))
		self.getSymbol()

	def isEmpty(self):
		return len(self.tokens) == 0

	def undo(self):
		self.tokens.append(self.last)
		self.last = None

	def getSymbol(self):
		if len(self.tokens) == 0:
			self.last = None
			self.token = None
			return None
		self.last = self.tokens[-1]
		self.token = self.last
		return self.tokens.pop()

	'''
	CompUnit -> FuncDef
	'''
	def CompUnit(self):
		self.FuncDef()
		if self.token == None:
			exit(0)
		else:
			exit(1)
	
	'''
	FuncDef  -> FuncType Ident '(' ')' Block
	'''
	def FuncDef(self):
		print("define dso_local ", file = self.outputfile, end = '')
		self.FuncType()
		
		if self.token == None or self.token.type != 'Main':
			exit(1)
		print("@main ", file = self.outputfile, end = '')
		self.getSymbol()

		if self.token == None or self.token.type != 'LPar':
			exit(1)
		print("(", file = self.outputfile, end = '')
		self.getSymbol()
		
		if self.token == None or self.token.type != 'RPar':
			exit(1)
		print(")", file = self.outputfile, end = '')
		self.getSymbol()
		
		self.Block()

	'''
	FuncType -> 'int'
	'''
	def FuncType(self):
		if self.token == None or self.token.type != 'Int':
			exit(1)
		print("i32 ", file = self.outputfile, end = '')
		self.getSymbol()
	
	'''
	Block -> '{' Stmt '}'
	'''
	def Block(self):
		if self.token == None or self.token.type != 'LBrace':
			exit(1)
		print("{\n", file = self.outputfile, end = '')
		self.getSymbol()

		self.Stmt()
		if self.token == None or self.token.type != 'RBrace':
			exit(1)
		print("}\n", file = self.outputfile, end = '')
		self.getSymbol()

	'''
	Stmt -> 'return' Exp ';'
	'''
	def Stmt(self):
		if self.token == None or self.token.type != 'Return':
			exit(1)
		print("ret ", file = self.outputfile, end = '')
		self.getSymbol()

		'''
		if self.token == None or self.token.type != 'Number':
			exit(1)
		print("i32 %d"%(self.token.value), file = self.outputfile, end = '')
		self.getSymbol()
		'''

		if self.token == None or self.token.type != 'Semicolon':
			exit(1)
		print("\n", file = self.outputfile, end = '')
		self.getSymbol()
	
	'''
	Exp	-> AddExp
	'''
	def Exp(self):
		pass

	'''
	AddExp	-> MulExp 
            | AddExp ('+' | '−') MulExp
	'''
	def AddExp(self):
		pass

	'''
	MulExp  -> UnaryExp
            | MulExp ('*' | '/' | '%') UnaryExp
	'''
	def MulExp(self):
		pass

	'''
	UnaryExp	-> PrimaryExp | UnaryOp UnaryExp
	'''
	def UnaryExp(self):
		
		pass
	
	'''
	PrimaryExp -> '(' Exp ')' | Number
	'''
	def PrimaryExp(self):
		if self.token == None or self.token.type not in ['LPar', 'Number']:
			exit(1)
		if self.token.type == 'Number':
			num = str(self.token.value)
			self.getSymbol()
			return num
		else:
			self.getSymbol()
			exp = self.Exp()
			if self.token.type != 'Rpar':
				exit(1)
			self.getSymbol()
			return '(' + exp + ')'

	'''
	UnaryOp	-> '+' | '-'
	'''
	def UnaryOp(self):
		if self.token == None or self.token.type not in ['Plus', 'Minus']:
			exit(1)
		op = self.tolen.value
		self.getSymbol()
		return op
		