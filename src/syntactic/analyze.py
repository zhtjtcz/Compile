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
		print("ComUnit!")
		self.FuncDef()
	
	'''
	FuncDef  -> FuncType Ident '(' ')' Block
	'''
	def FuncDef(self):
		print("Funcdef!")
		self.FuncType()
		if self.token == None or self.token.name != 'Main':
			exit(1)
		self.getSymbol()
		if self.token == None or self.token.name != 'LPar':
			exit(1)
		self.getSymbol()
		if self.token == None or self.token.name != 'RPar':
			exit(1)
		self.getSymbol()
		self.Block()

	'''
	FuncType -> 'int'
	'''
	def FuncType(self):
		print("FuncType!")
		if self.token == None or self.token.name != 'Int':
			exit(1)
		self.getSymbol()
	
	'''
	Block -> '{' Stmt '}'
	'''
	def Block(self):
		print("Block!")
		if self.token == None or self.token.name != 'LBrace':
			exit(1)
		self.getSymbol()
		self.Stmt()
		if self.token == None or self.token.name != 'RBrace':
			exit(1)
		self.getSymbol()

	'''
	Stmt -> 'return' Number ';'
	'''
	def Stmt(self):
		print("Stmt!")
		if self.token == None or self.token.name != 'Return':
			exit(1)
		self.getSymbol()
		if self.token == None or self.token.lexeme != 'Number':
			exit(1)
		self.getSymbol()
		if self.token == None or self.token.name != 'Semicolon':
			exit(1)
		self.getSymbol()