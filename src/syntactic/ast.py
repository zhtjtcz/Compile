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

def getPos(x : Node):
	size = []
	for i in x.children:
		exp(i)
		size.append(i.name)
	return size

def exp(x : Node):
	if x.type == 'Exp' or x.type == 'ConstExp':
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
			if x.children[0].name not in table.function.keys():
				exit(1)
			x.name = table.create_val()
			print('%s = call i32 @%s()'%(x.name, x.children[0].name), file = outputFile)
			# Ident LPar RPar
		elif len(x.children) == 4:
			exp(x.children[2])
			if x.children[0].name in ['putint', 'putch']:
				print('call void @%s(i32 %s)'%(x.children[0].name, x.children[2].children[0].name), file = outputFile)
			else:
				if x.children[0].name not in table.function.keys():
					exit(1)
				p = []
				paramstype = table.function[x.children[0].name][1]
				paramstype = [i[1] for i in paramstype]
				for son in range(len(x.children[2].children)):
					p.append(' '+ paramstype[son] + ' ' + x.children[2].children[son].name)
				if table.function[x.children[0].name][0] == 'void':
					print('call void ', end = '', file = outputFile)
				else:
					x.name = table.create_val()
					print('%s = call i32 '%(x.name), end = '', file = outputFile)
				print('@%s( %s )'%(x.children[0].name, ','.join(p)), file = outputFile)
			# Ident LPar FuncRParams RPar
	elif x.type == 'PrimaryExp':
		if len(x.children) == 1:
			if x.children[0].type == 'Number':
				x.name = table.create_val()
				print(x.name, '= add i32', '0 ,', str(x.children[0].value), file = outputFile)
			else:
				if len(x.children[0].children) == 0:
					if table.find_val_name(table.tree, x.children[0].name) != None:
						table.create_reg(x.children[0].name)
						node = table.find_val_name(table.tree, x.children[0].name)
						print('%s = load i32, i32* %s'%(table.get_reg(x.children[0].name), node.table[x.children[0].name]), file = outputFile)
						x.name = table.get_reg(x.children[0].name)
					else:
						node = table.find_array_name(table.tree, x.children[0].name)
						new = table.create_val()
						out = node.array[x.children[0].name][1]
						x.name = table.create_val()
						print("%s = getelementptr inbounds %s, %s* %s, %s"%(x.name, arrayOut(out), arrayOut(out), node.array[x.children[0].name][0], posOut([0, 0])),
							file = outputFile)
					# LVal or ARRAY NAME!
				elif table.find_array_name(table.tree, x.children[0].name) == None:
					node = table.find_pointer(table.tree, x.children[0].name)
					point = table.create_val()
					p = table.create_val()
					print('%s = load i32*, i32** %s'%(p, node.pointer[x.children[0].name]), file = outputFile)
					pos = posOut(getPos(x.children[0].children[0]))
					print('%s = getelementptr inbounds i32, i32* %s, %s'%(point, p, pos), file = outputFile)
					x.name = table.create_val()
					print('%s = load i32, i32* %s'%(x.name, point), file = outputFile)
					# Funcion array
				else:
					node = table.find_array_name(table.tree, x.children[0].name)
					pos = getPos(x.children[0].children[0])
					new = table.create_val()
					out = node.array[x.children[0].name][1]
					if len(out) == len(pos):
						out = arrayOut(out)
						print("%s = getelementptr inbounds %s, %s* %s, %s"%(new, out, out, node.array[x.children[0].name][0], posOut([0] + pos)),
							file = outputFile)
						x.name = table.create_val()
						print("%s = load i32, i32* %s"%(x.name, new), file = outputFile)
					else:
						pointer = table.create_val()
						print("%s = getelementptr inbounds %s, %s* %s, %s"%(pointer, arrayOut(out), arrayOut(out), node.array[x.children[0].name][0], posOut([0] + pos)),
							file = outputFile)
						x.name = table.create_val()
						print("%s = getelementptr inbounds %s, %s* %s, %s"%(x.name, arrayOut(out[-1]), arrayOut(out[-1]), pointer, posOut([0, 0])),
							file = outputFile)
						# Array pointer!
					# Array
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

def arrayOut(s):
	out = 'i32'
	if isinstance(s, int):
		s = [s]
	for i in range(len(s)-1, -1, -1):
		out = '[' + str(s[i]) + ' x ' + out + ']'
	return out

def appendArray(size, value):
	if len(size) == 2:
		while len(value) < size[0]:
			value.append([0 for i in range(size[1])].copy())
	if len(size) == 1:
		while len(value) < size[0]:
			value.append(0)
	else:
		for i in range(len(value)):
			appendArray(size[1:], value[i])

def initValue(x : Node):
	if x.type == 'ConstInitVals':
		return ','.join([initValue(x.children[i]) for i in range(len(x.children))])
	elif x.type == 'ConstInitVal':
		if len(x.children) == 0:
			return '[]'
		elif len(x.children) == 1:
			if table.tree.fa == None:
				return str(globalCal(x.children[0]))
				# Golbal
			else:
				exp(x.children[0])
				s = x.children[0].name
				return s[2:] if s[0] == '%' else s
				# Value
		else:
			return '[' + str(initValue(x.children[1])) + ']'

def posOut(pos : list):
	a = ['i32 ' + str(i) for i in pos]
	return ', '.join(a)

def fillArray(name, size, value, pos, out):
	if len(size) == 1:
		for i in range(size[0]):
			if value[i]:
				x = table.create_val()
				print("%s = getelementptr inbounds %s, %s* %s, %s"%(x, out, out, name, posOut(pos + [i])), file = outputFile)
				print("store i32 %%x%d, i32* %s"%(value[i], x), file = outputFile)
		# Fill it
	else:
		for i in range(size[0]):
			fillArray(name, size[1:], value[i], pos + [i], out)

def vardef(x : Node):
	val = x.children[0]
	if (len(x.children) == 2 and x.children[1].type == 'ConstSubs') or len(x.children) == 3:
		if val.name in table.tree.table.keys() or val.name in table.tree.const.keys():
			exit(1)
		if val.name in table.tree.array.keys() or val.name in table.tree.const_array.keys():
			exit(1)
		size = [globalCal(i) for i in x.children[1].children]
		name = table.create_array(val.name, size, False)
		if len(x.children) == 3:
			value = eval(initValue(x.children[2]))
			appendArray(size, value)
			fillArray(name, size, value, [0], arrayOut(size))
	else:
		val.add = table.create_val(val.name)
		if len(x.children) > 1:
			exp(x.children[1].children[0])
			s = x.children[1].children[0]
			# s -> Exp
			print('store i32', s.name, ', i32*', val.add, file = outputFile)
			table.create_reg(val.name)

def constdef(x : Node):
	val = x.children[0]
	if (len(x.children) == 2 and x.children[1].type == 'ConstSubs') or len(x.children) == 3:
		if val.name in table.tree.table.keys() or val.name in table.tree.const.keys():
			exit(1)
		if val.name in table.tree.array.keys() or val.name in table.tree.const_array.keys():
			exit(1)
		size = [globalCal(i) for i in x.children[1].children]
		value = eval(initValue(x.children[2]))
		appendArray(size, value)
		name = table.create_array(val.name, size, True, value)
		fillArray(name, size, value, [0], arrayOut(size))
	else:
		val.add = table.create_val(val.name)
		checkCanCal(x.children[1].children[0])
		value = globalCal(x.children[1].children[0].children[0])
		# s -> Addexp
		print('store i32', value, ', i32*', val.add, file = outputFile)
		table.create_reg(val.name)
		table.insert_const(val.name, value)

def vardecl(x : Node):
	for i in x.children:
		vardef(i)

def constdecl(x : Node):
	for i in x.children:
		constdef(i)

def globalCal(x : Node):
	if x.type == 'Exp' or x.type == 'ConstExp':
		return globalCal(x.children[0])
	elif x.type == 'AddExp':
		if len(x.children) == 1:
			return globalCal(x.children[0])
		else:
			a = globalCal(x.children[0])
			b = globalCal(x.children[2])
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
				return a//b
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
				if table.find_const_name(table.tree, x.children[0].name) == None:
					exit(1)
				node = table.find_const_name(table.tree, x.children[0].name)
				return node.const[x.children[0].name]
				# Val
		else:
			return globalCal(x.children[1])
	elif x.type == 'FuncRParams':
		exit(1)

def initArray(size, value):
	if len(size) == 1:
		if value.count(0) == len(value) and len(value) > 100:
			print("zeroinitializer", file = outputFile, end = '')
		else:
			print('[' +','.join(['i32 ' + str(i) for i in value]) + ']', file = outputFile, end ='')
	else:
		print('[', file = outputFile, end =' ')
		for i in range(len(value)):
			print(arrayOut(size[1:]), file = outputFile, end =' ')
			initArray(size[1:], value[i])
			if i != len(value) - 1:
				print(file = outputFile, end =', ')
		print(']', file = outputFile, end =' ')

def globalArray(x : Node):
	name = '@' + x.children[0].name
	size = [globalCal(i) for i in x.children[1].children]
	print('%s = dso_local global %s'%(name, arrayOut(size)), file = outputFile, end = ' ')
	if len(x.children) == 3:
		value = eval(initValue(x.children[2]))
	else:
		value = []
	if value == []:
		value = [0 for i in range(size[-1])]
		for i in range(len(size)-2, -1, -1):
			value = [value.copy() for j in range(size[i])]
	appendArray(size, value)
	initArray(size, value)
	print(file = outputFile)
	table.tree.array[x.children[0].name] = (name, size, value)
	# Const global array

def globalConst(x : Node):
	if x.children[0].name in table.tree.table.keys():
		exit(1)
	name = '@' + x.children[0].name
	if len(x.children) == 2:
		val = globalCal(x.children[1].children[0].children[0])
		print("%s = dso_local constant i32 %d"%(name, val), file = outputFile)
		globals[x.children[0].name] = val
		table.tree.const[x.children[0].name] = val
		table.tree.table[x.children[0].name] = name
		# Const global Val
	else:
		globalArray(x)

def globalVal(x : Node):
	if x.children[0].name in table.tree.table.keys():
		exit(1)
	name = '@' + x.children[0].name
	if (len(x.children) == 2 and x.children[1].type == 'InitVal') or len(x.children) == 1:
		table.tree.table[x.children[0].name] = name
		val = 0
		if len(x.children) != 1:
			val = globalCal(x.children[1].children[0].children[0])
		print("%s = dso_local global i32 %d"%(name, val), file = outputFile)
		globals[x.children[0].name] = val
	else:
		if x.children[0].name in table.tree.array.keys() or x.children[0].name in table.tree.const_array.keys():
			exit(1)
		globalArray(x)

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

def decl(x : Node):
	if x.children[0].type == 'ConstDecl':
		constdecl(x.children[0])
	else:
		vardecl(x.children[0])

def logicExp(x : Node):
	if x.type == 'LOrExp':
		logicExp(x.children[0])
		if len(x.children) == 1:
			x.name = x.children[0].name
		else:
			logicExp(x.children[1])
			x.name = table.create_val()
			print("%s = or i32 %s, %s"%(x.name, x.children[0].name, x.children[1].name), file = outputFile)
			# x must be i32!
	elif x.type == 'LAndExp':
		logicExp(x.children[0])
		if len(x.children) == 1:
			x.name = x.children[0].name
			x.isBool = x.children[0].isBool
			if x.isBool == True:
				transBooltoInt(x)
		else:
			logicExp(x.children[1])
			for i in range(2):
				if x.children[i].isBool == False:
					transInttoBool(x.children[i])
			x.name = table.create_val()
			print("%s = and i1 %s, %s"%(x.name, x.children[0].name, x.children[1].name), file = outputFile)
			transBooltoInt(x)
			x.isBool = False
			# x must be i32!
	elif x.type == 'EqExp':
		logicExp(x.children[0])
		if len(x.children) == 1:
			x.name = x.children[0].name
			x.isBool = x.children[0].isBool
		else:
			x.name = table.create_val()
			logicExp(x.children[2])
			for i in range(0,4,2):
				if x.children[i].isBool == True:
					transBooltoInt(x.children[i])
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

	if len(x.children) == 1 and x.children[0] == 'return':
		if table.funcType == 'Int':
			exit(1)
		print('ret void', file = outputFile)
		return
	# return;

	if len(x.children) == 1 and x.children[0].type in ['break', 'continue']:
		if x.children[0].type == 'break':
			print("br label %s"%(labelTree.node.breakLabel), file = outputFile)
		else:
			print("br label %s"%(labelTree.node.continueLabel), file = outputFile)
		return
	# break; or continue;

	if len(x.children) == 1 and x.children[0].type == 'Exp':
		exp(x.children[0])
		return
	# exp;

	if len(x.children) == 1 and x.children[0].type == 'Block':
		table.into_block()
		blockItems(x.children[0].children[0])
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
		if table.funcType == 'Void':
			exit(1)
		exp(x.children[1])
		print('ret i32', file = outputFile, end = ' ')
		print(x.children[1].name, file = outputFile)
		return
	# return exp;

	if len(x.children) == 3:
		val = x.children[0]
		if len(x.children[0].children) == 0:
			if table.find_val_name(table.tree, val.name) == None:
				exit(1)
			if table.find_const_name(table.tree, val.name) != None:
				exit(1)
			# Can't find the value
			exp(x.children[2])
			node = table.find_val_name(table.tree, val.name)
			print('store i32', x.children[2].name, ', i32*', node.table[val.name], file = outputFile)
			return
		else:
			if table.find_array_name(table.tree, val.name) == None:
				exit(1)
			node = table.find_array_name(table.tree, val.name)
			exp(x.children[2])

			pos = posOut([0] + getPos(val.children[0]))
			new = table.create_val()
			out = arrayOut(node.array[val.name][1])
			print("%s = getelementptr inbounds %s, %s* %s, %s"%(new, out, out, node.array[val.name][0], pos),
				file = outputFile)
			print("store i32 %s , i32* %s"%(x.children[2].name, new), file = outputFile)
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

def getFuncParams(x : Node):
	result = []
	for son in x.children:
		name = son.children[1]
		s = '%x' + str(table.id)
		table.id += 1
		type = 'i32' if len(son.children) == 2 else 'i32*'
		result.append((name, type, s))
	return result

def funcDef(x : Node):
	name = x.children[1].name
	if  name in table.function.keys():
		exit(1)
	print("define dso_local ", end = '', file = outputFile)
	table.into_block()
	if x.children[0].type == 'Int':
		print('i32 ', end = '', file = outputFile)
	else:
		print('void ', end = '', file = outputFile)

	if len(x.children) == 3:
		table.function[name] = (x.children[0].type, [])
		print("@%s(){"%(name), file = outputFile)
	else:
		params = getFuncParams(x.children[2])
		table.function[name] = (x.children[0].type, params)
		types = [i[1] + ' ' + i[2] for i in params]
		print("@%s( %s ){"%(name, ','.join(types)), file = outputFile)
		for p in params:
			if p[1] == 'i32*':
				s = '%x' + str(table.id)
				table.id += 1
				print('%s = alloca i32*'%(s), file = outputFile)
				print('store i32* %s, i32** %s'%(p[2], s), file = outputFile)
				table.tree.pointer[p[0]] = s
			else:
				s = table.create_val(p[0])
				print('store i32 %s, i32* %s'%(p[2] ,s), file = outputFile)
			# Create params value as local value
	
	table.funcType = x.children[0].type
	blockItems(x.children[-1].children[0])
	if x.children[0].type == 'Int':
		print('ret i32 0', file = outputFile)
	else:
		print('ret void', file = outputFile)
	table.out_block()
	
	print('}\n', file = outputFile)

def dfs(x : Node):
	if x.type == 'CompUnit':
		dfs(x.children[0])
	elif x.type == 'Definelist':
		for son in x.children:
			if son.children[0].type == 'Decl':
				globalDefine(son.children[0])
			else:
				funcDef(son.children[0])
	elif x.type == 'Block':
		table.into_block()
		blockItems(x.children[0])
		table.out_block()
	else:
		print("Some error!")
		exit(1)
