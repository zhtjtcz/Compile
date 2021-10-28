class Node():
	def __init__(self, type, children = [], name = '', value = 0):
		self.type = type
		self.children = children
		self.name = name
		self.value = value

	def dfs_test(self, x, d, fa):
		print(x.type, d, end = ' ')
		if fa == None:
			print('')
		else:
			print('father := ', fa.type)
		for i in x.children:
			self.dfs_test(i, d+1, x)

	def __str__(self):
		return self.type + '    ' + self.name + '    ' + str(self.value)

# TODO more class extend from node?