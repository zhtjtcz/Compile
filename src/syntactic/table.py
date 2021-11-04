from values import *

class Table():
	def __init__(self):
		self.table = {}
		self.reg = {}
		self.const = {}
		self.id = 1

	def create_val(self, name = None):
		if name == None:
			s = '%x' + str(self.id)
			self.id += 1
			return s
			# Simply exp or caclulation result
		else:
			if name in self.table.keys():
				exit(1)
			else:
				s = '%x' + str(self.id)
				self.table[name] = s
				self.id += 1
				print(s, '= alloca i32', file = outputFile)
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

	def create_reg(self, name = None):
		if name == None or name not in self.table.keys():
			exit(1)
		else:
			self.reg[name] = '%x' + str(self.id)
			self.id += 1

	def get_reg(self, name = None):
		if name == None or name not in self.table.keys():
			exit(1)
		else:
			return self.reg[name]

	def insert_const(self, name = None):
		if name == None or name in self.const.keys():
			exit(1)
		self.const[name] = True

	def create_flag(self):
		s = '%x' + str(self.id)
		self.id += 1
		return s
	# Goto flag

table = Table()
