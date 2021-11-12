from values import *

class BlockTree():
	def __init__(self):
		self.fa = None
		self.table = {}
		self.reg = {}
		self.const = {}

class Table():
	def __init__(self):
		'''
		self.table = {}
		self.reg = {}
		self.const = {}
		'''
		self.tree = BlockTree()
		self.id = 1

	def create_val(self, name = None):
		if name == None:
			s = '%x' + str(self.id)
			self.id += 1
			return s
			# Simply exp or caclulation result
		else:
			if name in self.tree.table.keys():
				exit(1)
			else:
				s = '%x' + str(self.id)
				self.tree.table[name] = s
				self.id += 1
				print(s, '= alloca i32', file = outputFile)
				return s
				# Ident
	
	def get_val(self, name = None):
		if name == None:
			exit(1)
		else:
			if name not in self.tree.table.keys():
				exit(1)
			else:
				return self.tree.table[name]

	def create_reg(self, name = None):
		if name == None or name not in self.tree.table.keys():
			exit(1)
		else:
			self.tree.reg[name] = '%x' + str(self.id)
			self.id += 1

	def get_reg(self, name = None):
		if name == None or name not in self.tree.table.keys():
			exit(1)
		else:
			return self.tree.reg[name]

	def insert_const(self, name = None):
		if name == None or name in self.tree.const.keys():
			exit(1)
		self.tree.const[name] = True

	def create_flag(self):
		s = '%x' + str(self.id)
		self.id += 1
		return s
	# Goto flag

	def into_block(self):
		node = BlockTree()
		node.fa = self.tree
		node.reg = self.tree.reg
		node.table = self.tree.table
		node.const = self.tree.const
		self.tree = node
	
	def out_block(self):
		self.tree = self.tree.fa
	
table = Table()
