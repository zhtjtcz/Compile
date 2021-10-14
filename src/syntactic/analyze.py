class Analyzer:
	def __init__(self, tokens, outputfile):
		self.tokens = tokens
		self.ftpken = None
		self.last = None
		self.outputfile = outputfile
	
	def isEmpty(self):
		return len(self.tokens) == 0

	def undo(self):
		self.tokens.append(self.last)
		self.last = None

	def getSymbol(self):
		if len(self.tokens) == 0:
			exit(-1)
		self.last = self.tokens[-1]
		return self.tokens.pop()
	
	def CompUnit(self):
		print("ComUnit!")
	
	

	