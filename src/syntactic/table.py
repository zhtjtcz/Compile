from values import *

class BlockTree():
	def __init__(self):
		self.fa = None
		self.table = {}
		self.reg = {}
		self.const = {}
		self.array = {}
		self.pointer = {}
		self.const_array = {}

class Table():
	def __init__(self):
		self.tree = BlockTree()
		self.function = {'getint':'', 'getch':''}
		self.funcType = 'Int'
		self.id = 1

	def create_val(self, name = None):
		if name == None:
			s = '%x' + str(self.id)
			self.id += 1
			return s
			# Simply exp or caclulation result
		else:
			if name in self.tree.table.keys() or name in self.tree.array.keys() or name in self.tree.const_array.keys():
				exit(1)
			else:
				s = '%x' + str(self.id)
				self.tree.table[name] = s
				self.id += 1
				print(s, '= alloca i32', file = outputFile)
				return s
				# Ident
	
	def create_array(self, name, size, const = False, value = None):
		if name in self.tree.table.keys() or name in self.tree.array.keys() or name in self.tree.const_array.keys():
			exit(1)
		else:
			s = '%x' + str(self.id)
			self.id += 1
			print("%s = alloca %s"%(s, size), file = outputFile)
			self.tree.array[name] = (s, size)
			if const == True:
				self.tree.const_array[name] = (s, size, value)
			return s

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

	def insert_const(self, name = None, value = 0):
		if name == None or name in self.tree.const.keys():
			exit(1)
		self.tree.const[name] = value

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
	
	def find_array_name(self, x : BlockTree, name):
		if x == None:
			return None
		if name in x.array.keys():
			return x
		else:
			return self.find_array_name(x.fa, name)

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
		node.fa = self.tree
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
