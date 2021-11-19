from values import *
from syntactic.node import Node
from syntactic.table import table,globals,labelTree

def transInttoBool(x : Node):
	s = table.create_val()
	print("%s = icmp ne i32 %s, 0"%(s, x.name), file = outputFile)
	x.name = s
	x.isBool = True

def transBooltoInt(x : Node):
	s = table.create_val()
	print("%s = zext i1 %s to i32"%(s, x.name), file = outputFile)
	x.name = s
	x.isBool = False

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
			elif x.children[0].type == '-':
				print(x.name, '= sub i32 0,', x.children[1].name, file = outputFile)
			elif x.children[0].type == '!':
				print("%s = icmp eq i32 %s, 0"%(x.name, x.children[1].name), file = outputFile)
				transBooltoInt(x)
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
				table.create_reg(x.children[0].name)
				node = table.find_val_name(table.tree, x.children[0].name)
				print('%s = load i32, i32* %s'%(table.get_reg(x.children[0].name), node.table[x.children[0].name]), file = outputFile)
				x.name = table.get_reg(x.children[0].name)
				# Val
		else:
			exp(x.children[1])
			x.name = x.children[1].name
	elif x.type == 'FuncRParams':
		for i in x.children:
			exp(i)

def checkCanCal(x : Node):
	if x == None:
		return
	if x.type == 'PrimaryExp' and x.children[0].type == 'LVal':
		if table.find_const_name(table.tree, x.children[0].name) == None:
			exit(1)
		# Calculate the value using no const val
	for i in x.children:
		checkCanCal(i)

def vardef(x : Node):
	val = x.children[0]
	val.add = table.create_val(val.name)
	if len(x.children) > 1:
		exp(x.children[1].children[0])
		s = x.children[1].children[0]
		# s -> Exp
		print('store i32', s.name, ', i32*', val.add, file = outputFile)
		table.create_reg(val.name)

def constdef(x : Node):
	val = x.children[0]
	val.add = table.create_val(val.name)
	checkCanCal(x.children[1].children[0])
	exp(x.children[1].children[0].children[0])
	s = x.children[1].children[0].children[0]
	# s -> Addexp
	print('store i32', s.name, ', i32*', val.add, file = outputFile)
	table.create_reg(val.name)
	table.insert_const(val.name)

def vardecl(x : Node):
	for i in x.children:
		vardef(i)

def constdecl(x : Node):
	for i in x.children:
		constdef(i)

def globalCal(x : Node):
	if x.type == 'Exp':
		return globalCal(x.children[0])
	elif x.type == 'AddExp':
		if len(x.children) == 1:
			return globalCal(x.children[0])
		else:
			a = globalCal(x.children[2])
			b = globalCal(x.children[0])
			return a+b if x.children[1].type == '+' else a-b
	elif x.type == 'MulExp':
		if len(x.children) == 1:
			return globalCal(x.children[0])
		else:
			a = globalCal(x.children[2])
			b = globalCal(x.children[0])
			if x.children[1].type == '*':
				return a*b
			elif x.children[1].type == '/':
				return a/b
			else:
				return a%b
	elif x.type == 'UnaryExp':
		if len(x.children) == 1:
			return globalCal(x.children[0])
		elif len(x.children) == 2:
			a = globalCal(x.children[1])
			if x.children[0].type == '+':
				return a
			elif x.children[0].type == '-':
				return -a
			elif x.children[0].type == '!':
				exit(1)
		else:
			exit(1)
			# No function
	elif x.type == 'PrimaryExp':
		if len(x.children) == 1:
			if x.children[0].type == 'Number':
				return int(str(x.children[0].value))
			else:
				if x.children[0].name not in table.tree.const.keys():
					exit(1)
				return globals[x.children[0].name]
				# Val
		else:
			return globalCal(x.children[1])
	elif x.type == 'FuncRParams':
		exit(1)

def globalConst(x : Node):
	if x.children[0].name in table.tree.table.keys():
		exit(1)
	name = '@' + x.children[0].name
	# checkCanCal(x.children[1].children[0])
	val = globalCal(x.children[1].children[0].children[0])
	print("%s = dso_local constant i32 %d"%(name, val), file = outputFile)
	globals[x.children[0].name] = val
	table.tree.const[x.children[0].name] = True
	table.tree.table[x.children[0].name] = name

def globalVal(x : Node):
	if x.children[0].name in table.tree.table.keys():
		exit(1)
	name = '@' + x.children[0].name	
	table.tree.table[x.children[0].name] = name
	val = 0
	if len(x.children) != 1:
		checkCanCal(x.children[1].children[0])
		val = globalCal(x.children[1].children[0].children[0])
	print("%s = dso_local global i32 %d"%(name, val), file = outputFile)
	globals[x.children[0].name] = val

def globalDefine(x : Node):
	for i in x.children[0].children:
		if x.children[0].type == 'ConstDecl':
			globalConst(i)
		else:
			globalVal(i)

def blockItems(x : Node):
	for i in x.children:
		print(i.type)
		if i.type == 'Decl':
			decl(i)
		else:
			stmt(i)

def block(x : Node):
	blockItems(x.children[0])

def decl(x : Node):
	if x.children[0].type == 'ConstDecl':
		constdecl(x.children[0])
	else:
		vardecl(x.children[0])

def logicExp(x : Node):
	if x.type == 'LOrExp':
		if len(x.children) == 1:
			logicExp(x.children[0])
			x.name = x.children[0].name
		else:
			logicExp(x.children[0])
			logicExp(x.children[1])
			x.name = table.create_val()
			print("%s = or i32 %s, %s"%(x.name, x.children[0].name, x.children[1].name), file = outputFile)
			# x must be i32!
	elif x.type == 'LAndExp':
		if len(x.children) == 1:
			logicExp(x.children[0])
			x.name = x.children[0].name
			x.isBool = x.children[0].isBool
			if x.isBool == True:
				transBooltoInt(x)
		else:
			logicExp(x.children[0])
			logicExp(x.children[1])
			if x.children[0].isBool == True:
				transBooltoInt(x.children[0])
			if x.children[1].isBool == True:
				transBooltoInt(x.children[1])
			x.name = table.create_val()
			print(x.children[0].name, x.children[0].isBool, x.children[1].isBool)
			print("%s = and i32 %s, %s"%(x.name, x.children[0].name, x.children[1].name), file = outputFile)
			x.isBool = False
			# x must be i32!
	elif x.type == 'EqExp':
		if len(x.children) == 1:
			logicExp(x.children[0])
			x.name = x.children[0].name
			x.isBool = x.children[0].isBool
		else:
			x.name = table.create_val()
			logicExp(x.children[0])
			logicExp(x.children[2])
			if x.children[0].isBool == True:
				transBooltoInt(x.children[0])
			if x.children[2].isBool == True:
				transBooltoInt(x.children[2])

			if x.children[1].type == '==':
				print("%s = icmp eq i32 %s, %s"%(x.name, x.children[0].name, x.children[2].name), file = outputFile)
			elif x.children[1].type == '!=':
				print("%s = icmp ne i32 %s, %s"%(x.name, x.children[0].name, x.children[2].name), file = outputFile)
			x.isBool = True
		# 需要确保这里返回的一定是 i1 类型
		# 上面只有逻辑运算
	elif x.type == 'RelExp':
		if len(x.children) == 1:
			exp(x.children[0])
			x.name = x.children[0].name
			x.isBool = False
		else:
			x.name = table.create_val()
			logicExp(x.children[0])
			exp(x.children[2])
			if x.children[0].isBool == True:
				transBooltoInt(x.children[0])
			# Bool check
			optable = {'<':'slt', '>':'sgt', '<=':'sle', '>=':'sge'}
			print("%s = icmp %s i32 %s, %s"%(x.name, optable[x.children[1].type], x.children[0].name, x.children[2].name), file = outputFile)
			x.isBool = True

def cond(x : Node):
	logicExp(x.children[0])
	x.name = x.children[0].name
	transInttoBool(x)

def stmt(x : Node):
	if len(x.children) == 0:
		return
	# ;

	if len(x.children) == 1 and x.children[0].type in ['break', 'continue']:
		if x.children[0].type == 'break':
			print("br label %s"%(labelTree.node.breakLabel), file = outputFile)
		else:
			print("br label %s"%(labelTree.node.continueLabel), file = outputFile)
	# break; or continue;

	if len(x.children) == 1 and x.children[0].type == 'Exp':
		exp(x.children[0])
		return
	# exp;

	if len(x.children) == 1 and x.children[0].type == 'Block':
		table.into_block()
		block(x.children[0])
		table.out_block()
		return
	# Block;

	if len(x.children) == 2 and x.children[0].type == 'Cond':
		Check = table.create_flag()
		Do = table.create_flag()
		Next  = table.create_flag()
		labelTree.intoWhile(continueLabel = Check, breakLabel = Next)

		print("br label %s"%(Check), file = outputFile)
		print(Check[1:] + ':', file = outputFile)
		cond(x.children[0])
		print("br i1 %s, label %s, label %s"%(x.children[0].name, Do, Next), file = outputFile)

		print(Do[1:] + ':', file = outputFile)
		stmt(x.children[1])
		print("br label %s"%(Check), file = outputFile)
		
		labelTree.outWhile()
		print(Next[1:] + ':', file = outputFile)
		return
	# While (Cond) Stmt;

	if len(x.children) == 2:
		exp(x.children[1])
		print('ret i32', file = outputFile, end = ' ')
		print(x.children[1].name, file = outputFile)
		return
	# return exp;

	if len(x.children) == 3:
		val = x.children[0]
		if table.find_val_name(table.tree, val.name) == None:
			exit(1)
		# Can't find the value
		exp(x.children[2])
		node = table.find_val_name(table.tree, val.name)
		print('store i32', x.children[2].name, ', i32*', node.table[val.name], file = outputFile)
		return
	# LVal Equal Exp Semicolon

	if len(x.children) == 4:
		Then = table.create_flag()
		Next = table.create_flag()
		cond(x.children[0])
		print("br i1 %s, label %s, label %s"%(x.children[0].name, Then, Next), file = outputFile)
		
		print(Then[1:] + ':', file = outputFile)
		stmt(x.children[1])
		print('br label', Next, file = outputFile)

		print(Next[1:] + ':', file = outputFile)
		return
	# If LPar Cond RPar Stmt

	if len(x.children) == 5:
		Then = table.create_flag()
		Else = table.create_flag()
		Next = table.create_flag()
		cond(x.children[0])
		print("br i1 %s, label %s, label %s"%(x.children[0].name, Then, Else), file = outputFile)
		
		print(Then[1:] + ':', file = outputFile)
		stmt(x.children[1])
		print('br label', Next, file = outputFile)

		print(Else[1:] + ':', file = outputFile)
		stmt(x.children[2])
		print('br label', Next, file = outputFile)

		print(Next[1:] + ':', file = outputFile)
		return
	# If LPar Cond RPar Stmt Else Stmt

def dfs(x : Node):
	if x.type == 'CompUnit':
		dfs(x.children[0])
	elif x.type == 'Definelist':
		for i in x.children[:-1]:
			globalDefine(i)
		dfs(x.children[-1])		# Main fuction define	
	elif x.type == 'FuncDef':
		print('define dso_local i32 @main(){', file = outputFile)
		dfs(x.children[-1])
		print('}', file = outputFile)
		# TODO check the ident -> lab x
	elif x.type == 'Block':
		table.into_block()
		block(x)
		table.out_block()
	else:
		print("Some error!")
		exit(1)
