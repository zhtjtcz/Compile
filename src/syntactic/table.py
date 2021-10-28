from values import *

class Table():
	def __init__(self):
		self.table = {}
		self.id = 1

	def create_val(self, name = None):
		if name == None:
			s = '%' + str(self.id)
			self.id += 1
			return s
			# Simply exp or caclulation result
		else:
			if name in self.table.keys():
				exit(1)
			else:
				s = '%' + str(self.id)
				self.id += 1
				return s
				# Ident
	
	def get_val(self, name = None):
		if name == None:
			exit(1)
		else:
			if name not in self.table.keys():
				exit(1)
			else:
				return self.table[name]

table = Table()