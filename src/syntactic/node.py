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

	def dfs_test(self, x, d, fa):
		try:
			print(x[0])
		except:
			pass
		if isinstance(x, str) == True:
			print(x, d, end = ' ')
		else:
			print(x.type, d, end = ' ')
			if fa == None:
				print('')
			else:
				print('father -> ', fa.type)
			for i in x.children:
				self.dfs_test(i, d+1, x)
	
	def __str__(self):
		return self.type + '    ' + self.name + '    ' + str(self.value)
