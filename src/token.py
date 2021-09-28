class Token:
	def __init__(self, s):
		self.s = s
	
	def IsEnd(self):
		return False

	def GetToken(self):
		return 's'