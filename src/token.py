SY_TABLE = {
	'=':'Assign', ';':'Semicolon', '(':'LPar', ')': 'RPar',
	'{':'LBrace', '}':'RBrace', '+':'Plus', '*':'Mult',
	'/':'Div', '<':'Lt', '>':'Gt', '==':'Eq'
}

KEY_TABLE = {
	'if':'If', 'else':'Else', 'while':'While', 'continue':'Continue',
	'return':'Return', 'break':'Break'
}

class Token:
	def __init__(self, s):
		self.lexeme = ''
		self.number  = '1'
		self.name = ''

		if s == 'Error!':
			self.lexeme = 'Err'
			return
		# TODO simply error

		if s in SY_TABLE.keys():
			self.lexeme = SY_TABLE[s]
		elif s in KEY_TABLE.keys():
			self.lexeme = KEY_TABLE[s]
		elif len(s) == 1 and s.isalpha() == False and s.isdigit() == False:
			self.lexeme = 'Err'
		else:
			if s.isdigit():
				self.lexeme = 'Number'
				self.number = s
			else:
				self.lexeme = 'Ident'
				self.name = s

	def __str__(self):
		if self.lexeme == 'Ident':
			return "Ident(%s)"%self.name
		elif self.lexeme == 'Number':
			return "Number(%s)"%self.number
		else:
			return self.lexeme