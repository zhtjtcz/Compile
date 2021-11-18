from values import *

class BlockTree():
	def __init__(self):
		self.fa = None
		self.table = {}
		self.reg = {}
		self.const = {}

class Table():
	def __init__(self):
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

	def create_reg(self, name = None):
		if name == None or self.find_val_name(self.tree, name) == None:
			exit(1)
		else:
			node = self.find_val_name(self.tree, name)
			node.reg[name] = '%x' + str(self.id)
			# Global val or local val
			# Insert into the father node
			self.id += 1

	def create_flag(self):
		s = '%x' + str(self.id)
		self.id += 1
		return s
	# Goto flag

	def insert_const(self, name = None):
		if name == None or name in self.tree.const.keys():
			exit(1)
		self.tree.const[name] = True

	def find_val_name(self, x : BlockTree, name):
		if x == None:
			return None
		if name in x.table.keys():
			return x
		else:
			return self.find_val_name(x.fa, name)
		# Find a val name in the block-tree
	
	def find_const_name(self, x : BlockTree, name):
		if x == None:
			return None
		if name in x.const.keys():
			return x
		else:
			return self.find_const_name(x.fa, name)
		# Find a const name in the block-tree

	def get_val(self, name = None):
		if name == None:
			exit(1)
		else:
			if self.find_val_name(name) == None:
				exit(1)
			else:
				node = self.find_val_name(self.tree, name)
				return node.table[name]

	def get_reg(self, name = None):
		if name == None or self.find_val_name(self.tree, name) == None:
			exit(1)
		else:
			node = self.find_val_name(self.tree, name)
			return node.reg[name]

	def into_block(self):
		node = BlockTree()
		node.table = {}
		node.reg = {}
		node.const = {}
		node.fa = self.tree
		# Must be shallow copy!
		self.tree = node
	
	def out_block(self):
		self.tree = self.tree.fa

class LabelTree():
	def __init__(self):
		self.fa = None
		self.node = None
		self.continueLabel = ''
		self.breakLabel = ''
	
	def intoWhile(self, continueLabel = '', breakLabel = ''):
		newNode = LabelTree()
		newNode.continueLabel = continueLabel
		newNode.breakLabel = breakLabel
		newNode.fa = self.node
		self.node = newNode

	def outWhile(self):
		self.node = self.node.fa

table = Table()
globals = {}
labelTree = LabelTree()
