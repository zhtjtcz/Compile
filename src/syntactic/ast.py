from values import *
from syntactic.node import Node
from syntactic.table import table

def block(x : Node):
	if x.type == 'Stmt':
		dfs(x.children[1])
		print('ret i32', file = outputFile, end = ' ')
		print(x.children[1].name, file = outputFile)
	elif x.type == 'Exp':
		dfs(x.children[0])
		x.name = x.children[0].name
	elif x.type == 'AddExp':
		if len(x.children) == 1:
			dfs(x.children[0])
			x.name = x.children[0].name
		else:
			dfs(x.children[2])
			dfs(x.children[0])
			x.name = table.create_val()
			if x.children[1].type == '+':
				print(x.name, '= add i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
			else:
				print(x.name, '= sub i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
	elif x.type == 'MulExp':
		if len(x.children) == 1:
			dfs(x.children[0])
			x.name = x.children[0].name
		else:
			dfs(x.children[2])
			dfs(x.children[0])
			x.name = table.create_val()
			if x.children[1].type == '*':
				print(x.name, '= mul i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
			elif x.children[1].type == '/':
				print(x.name, '= sdiv i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
			else:
				print(x.name, '= srem i32', x.children[0].name, ',', x.children[2].name, file = outputFile)
	elif x.type == 'UnaryExp':
		if len(x.children) == 1:
			dfs(x.children[0])
			x.name = x.children[0].name
		else:
			dfs(x.children[1])
			x.name = table.create_val()
			if x.children[0].type == '+':
				print(x.name, '= add i32 0,', x.children[1].name, file = outputFile)
			else:
				print(x.name, '= sub i32 0,', x.children[1].name, file = outputFile)
	elif x.type == 'PrimaryExp':
		if len(x.children) == 1:
			x.name = str(x.children[0].value)
		else:
			dfs(x.children[1])
			x.name = x.children[1].name
	elif x.type == 'Number':
		x.name = str(x.value)


def dfs(x : Node):
	if x.type == 'CompUnit':
		dfs(x.children[0])
	elif x.type == 'FuncDef':
		print('define dso_local i32 @main()', file = outputFile, end = '')
		dfs(x.children[-1])
		# TODO check the ident -> lab x
	elif x.type == 'Block':
		print('{', file = outputFile)
		block(x.children[1])
		print('}', file = outputFile)