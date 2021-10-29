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
		elif len(x.children) == 3:
			x.name = table.create_val()
			if x.children[0].name == 'getint':
				print('%s = call i32 @getint()'%(x.name), file = outputFile)
			elif x.children[0].name == 'getch':
				print('%s = call i32 @getch()'%(x.name), file = outputFile)
			# Ident LPar RPar
		elif len(x.children) == 4:
			exp(x.children[2])
			if x.children[0].name == 'putint':
				print('call void @putint(i32 %s)'%(x.children[2].children[0].name), file = outputFile)
			elif x.children[0].name == 'putch':
				print('call void @putch(i32 %s)'%(x.children[2].children[0].name), file = outputFile)
			# Ident LPar FuncRParams RPar
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
	elif x.type == 'FuncRParams':
		for i in x.children:
			exp(i)

def check_can_cal(x : Node):
	if x == None:
		return
	if x.type == 'PrimaryExp' and x.children[0].type == 'LVal':
		if x.children[0].name not in table.const.keys():
			exit(1)
		# Calculate the value using no const val
	for i in x.children:
		check_can_cal(i)

def vardef(x : Node):
	val = x.children[0]
	if len(x.children) == 1:
		val.add = table.create_val(val.name)
	else:
		val.add = table.create_val(val.name)
		exp(x.children[1].children[0])
		s = x.children[1].children[0]
		# s -> Exp
		print('store i32', s.name, ', i32*', val.add, file = outputFile)
		table.create_reg(val.name)
		print('%s = load i32, i32* %s'%(table.get_reg(val.name), val.add), file = outputFile)
		# Load it when create it

def constdef(x : Node):
	val = x.children[0]
	if len(x.children) == 1:
		val.add = table.create_val(val.name)
	else:
		val.add = table.create_val(val.name)
		check_can_cal(x.children[1].children[0])
		exp(x.children[1].children[0].children[0])
		s = x.children[1].children[0].children[0]
		# s -> Addexp
		print('store i32', s.name, ', i32*', val.add, file = outputFile)
		table.create_reg(val.name)
		table.insert_const(val.name)
		print('%s = load i32, i32* %s'%(table.get_reg(val.name), val.add), file = outputFile)
		# Load it when create it

def vardecl(x : Node):
	for i in x.children:
		vardef(i)

def constdecl(x : Node):
	for i in x.children:
		constdef(i)

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
		exp(x.children[0])
		return
	# exp;

	if len(x.children) == 2:
		exp(x.children[1])
		print('ret i32', file = outputFile, end = ' ')
		print(x.children[1].name, file = outputFile)
		return
	# return exp;

	if len(x.children) == 3:
		val = x.children[0]
		if val.name in table.const.keys() == True:
			exit(1)
		exp(x.children[2])
		print('store i32', x.children[2].name, ', i32*', table.table[val.name], file = outputFile)
		table.create_reg(val.name)
		print('%s = load i32, i32* %s'%(table.get_reg(val.name), table.table[val.name]), file = outputFile)
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