from lexical.token import Token
from values import *
from lexical.token import SY_TABLE,BREAK_TABLE

class Laxer:
	def __init__(self, s):
		self.code = s
		self.pre=''

	def isEnd(self):
		return len(self.code) == 0
	
	def getchar(self):
		if len(self.code) == 0:
			return ''
		ch = self.code[0]
		self.pre = ch
		self.code = self.code[1:]
		return ch

	def redo(self):
		self.code = self.pre + self.code
		self.pre = ''

	def getToken(self):
		while True:
			if self.isEnd():
				return ''
			# End of the code
			
			ch = self.getchar()
			if ch in BREAK_TABLE:
				continue
			self.redo()
			break
		
		ch = self.getchar()
		if ch in SY_TABLE.keys():
			return Token(ch)	# simple sign
		elif ch.isdigit():
			val = ch
			while self.isEnd() == False:
				ch = self.getchar()
				if ch in BREAK_TABLE or ch in SY_TABLE.keys():
					self.redo()
					break
				val = val + ch
			return Token(val)	# Number
		elif ch=='_' or ch.isalpha():
			val = ch
			while self.isEnd() == False:
				ch = self.getchar()
				if ch == '_' or ch.isdigit() or ch.isalpha():
					val += ch
				else:
					self.redo()
					break
			return Token(val)	# Symbol
		else:
			return Token('Error!')

def getTokens(input, outputFile):
	lex = Laxer(input)
	tokens = []
	while lex.isEnd() == False:
		token = lex.getToken()
		if token == '':
			break
		if LOCAL:
			print(token, file = outputFile)
		if token.lexeme == 'Err':
			exit(1)	# Token error
		else:
			tokens.append(token)
	return tokens