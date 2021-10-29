from values import *
from syntactic.node import Node
from syntactic.table import table

def exp(x : Node):
	if x.type == 'Exp':
		exp(x.children[0])
		x.name = x.children[0].name
	elif x.type == 'AddExp':
		if len(x.children) == 1:
			exp(x.children[0])
			x.name = x.children[0].name
		else:
			exp(x.children[2])
			exp(x.children[0])
			x.name = table.create_val()
			if x.children[1].type == '+':
				print(x.name, '= add i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
			else:
				print(x.name, '= sub i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
	elif x.type == 'MulExp':
		if len(x.children) == 1:
			exp(x.children[0])
			x.name = x.children[0].name
		else:
			exp(x.children[2])
			exp(x.children[0])
			x.name = table.create_val()
			if x.children[1].type == '*':
				print(x.name, '= mul i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
			elif x.children[1].type == '/':
				print(x.name, '= sdiv i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
			else:
				print(x.name, '= srem i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
	elif x.type == 'UnaryExp':
		if len(x.children) == 1:
			exp(x.children[0])
			x.name = x.children[0].name
		elif len(x.children) == 2:
			exp(x.children[1])
			x.name = table.create_val()
			if x.children[0].type == '+':
				print(x.name, '= add i32 0,', x.children[1].name, file = outputFile)
			else:
				print(x.name, '= sub i32 0,', x.children[1].name, file = outputFile)
		else:
			pass
			# TODO fuction call 
	elif x.type == 'PrimaryExp':
		if len(x.children) == 1:
			if x.children[0].type == 'Number':
				x.name = str(x.children[0].value)
			else:
				x.name = table.get_reg(x.children[0].name)
				# Val
		else:
			exp(x.children[1])
			x.name = x.children[1].name

def vardef(x : Node):
	val = x.children[0]
	if len(x.children) == 1:
		val.add = table.create_val(val.name)
	else:
		val.add = table.create_val(val.name)
		exp(x.children[1].children[0])
		s = x.children[1].children[0]
		print('store i32', s.name, ', i32*', val.add, file = outputFile)
		table.create_reg(val.name)
		print('%s = load i32, i32* %s'%(table.get_reg(val.name), val.add), file = outputFile)
		# Load it when create it

def vardecl(x : Node):
	for i in x.children:
		vardef(i)

def constdecl(x : Node):
	pass

def decl(x : Node):
	if x.children[0].type == 'ConstDecl':
		constdecl(x.children[0])
	else:
		vardecl(x.children[0])

def stmt(x : Node):
	if len(x.children) == 0:
		return
	# ;

	if len(x.children) == 1:
		return
	# exp; // ignore

	if len(x.children) == 2:
		exp(x.children[1])
		print('ret i32', file = outputFile, end = ' ')
		print(x.children[1].name, file = outputFile)
	# return exp;

	if len(x.children) == 3:
		val = x.children[0]
		if val.const == True:
			exit(1)
		exp(x.children[2])
		print('store i32', x.children[3].name, ', i32*', val.add, file = outputFile)
		table.create_reg(val.name)
		print('%s = load i32, i32* %s'%(table.get_reg(val.name), val.add), file = outputFile)
	# LVal Equal Exp Semicolon

def block(x : Node):
	for i in x.children:
		print(i.type)
		if i.type == 'Decl':
			decl(i)
		else:
			stmt(i)

def dfs(x : Node):
	if x.type == 'CompUnit':
		dfs(x.children[0])
	elif x.type == 'FuncDef':
		print('define dso_local i32 @main()', file = outputFile, end = '')
		dfs(x.children[-1])
		# TODO check the ident -> lab x
	elif x.type == 'Block':
		print('{', file = outputFile)
		block(x.children[0])
		print('}', file = outputFile)