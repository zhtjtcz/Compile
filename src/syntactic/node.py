class Node():
	def __init__(self, type, chidlren = [], name = None, number = 0):
		self.type = type
		self.children = chidlren
		self.name = name
		self.value = number

	def dfs_test(self):
		print(self)
		for i in self.children:
			self.dfs_test(i)

	def __str__(self):
		return self.type + self.name + str(self.value)

# TODO more class extend from node?