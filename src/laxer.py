from token import Token

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
			if ch in ['\n', '\t', ' ', '\r']:
				continue
			self.redo()
			break
		
		ch = self.getchar()
		if ch in [';', '(', ')', '{', '}', '+', '-', '*', '/', '<', '>']:
			return Token(ch)
		elif ch == '=':
			if self.getchar() == '=':
				return Token('==')
			else:
				self.redo()
				return Token('=')
		elif ch.isdigit():
			val = ch
			while self.isEnd() == False:
				ch = self.getchar()
				if ch.isdigit() == False:
					self.redo()
					break
				val = val + ch
			return Token(val)
			# Number
		elif ch=='_' or ch.isalpha():
			val = ch
			while self.isEnd() == False:
				ch = self.getchar()
				if ch == '_' or ch.isdigit() or ch.isalpha():
					val += ch
				else:
					self.redo()
					break
			return Token(val)
			# Symbol
		else:
			return Token('Error!')