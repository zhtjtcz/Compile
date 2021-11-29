class Node():
	def __init__(self, type, children = [], name = '', value = 0):
		self.type = type
		self.children = children
		self.name = name
		# If it's not ident, it may store the %x
		# If it's ident, it store the real name
		
		self.add = ''
		self.isBool = False
		self.value = value
	
	def __str__(self):
		return self.type + '    ' + self.name + '    ' + str(self.value)
