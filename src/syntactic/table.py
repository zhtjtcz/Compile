from values import *

class Table():
	def __init__(self):
		self.table = {}
		self.id = 1

	def create_val(self, name = None):
		s = '%x' + str(self.id)
		self.id += 1
		# print(s + ' = alloca i32', file = outputFile)
		return s

table = Table()