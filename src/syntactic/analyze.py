from values import *

class Analyzer:
	def __init__(self, tokens, outputfile):
		self.tokens = tokens
		self.ftpken = None
		self.last = None
		self.outputfile = outputfile
		self.getSymbol()
	
	def isEmpty(self):
		return len(self.tokens) == 0

	def undo(self):
		self.tokens.append(self.last)
		self.last = None

	def getSymbol(self):
		if len(self.tokens) == 0:
			self.last = None	
			return None
		self.last = self.tokens[-1]
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
		if self.token == None or self.token.name != 'Main':
			exit(1)
		print("@main ", file = self.outputfile, end = '')
		self.getSymbol()
		if self.token == None or self.token.name != 'LPar':
			exit(1)
		print("( ", file = self.outputfile, end = '')
		self.getSymbol()
		if self.token == None or self.token.name != 'RPar':
			exit(1)
		print(") ", file = self.outputfile, end = '')
		self.getSymbol()
		self.Block()

	'''
	FuncType -> 'int'
	'''
	def FuncType(self):
		if self.token == None or self.token.name != 'Int':
			exit(1)
		print("i32", file = self.outputfile, end = '')
		self.getSymbol()
	
	'''
	Block -> '{' Stmt '}'
	'''
	def Block(self):
		if self.token == None or self.token.name != 'LBrace':
			exit(1)
		print("{\n", file = self.outputfile, end = '')
		self.getSymbol()
		self.Stmt()
		if self.token == None or self.token.name != 'RBrace':
			exit(1)
		print("}\n", file = self.outputfile, end = '')
		self.getSymbol()

	'''
	Stmt -> 'return' Number ';'
	'''
	def Stmt(self):
		print("Stmt!")
		if self.token == None or self.token.name != 'Return':
			exit(1)
		print("ret ", file = self.outputfile, end = '')
		self.getSymbol()
		if self.token == None or self.token.lexeme != 'Number':
			exit(1)
		print("i32 %d"%(self.token.number), file = self.outputfile, end = '')
		self.getSymbol()
		if self.token == None or self.token.name != 'Semicolon':
			exit(1)
		self.getSymbol()