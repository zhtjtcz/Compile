def remove(s):
	if '//' not in s and '/*' not in s:
		return s
	out = ''
	flag = 0
	i = 0
	length = len(s)
	while i<length:
		if flag == 2 and s[i]=='*':
			if i+1<length and s[i+1]=='/':
				flag = 0
				i += 2
				continue
		if flag == 1 and s[i]=='\n':
			out += '\n'
			flag = 0
			i += 1
			continue
		if flag == 0 and s[i]=='/':
			if i+1<length and s[i+1]=='/':
				flag = 1
				i += 2
				continue
		if flag == 0 and s[i]=='/':
			if i+1<length and s[i+1]=='*':
				flag = 2
				i += 2
				continue
		if flag:
			i += 1
			continue
		out += s[i]
		i += 1
	# clear the note

	if flag:
		exit(1)
	# Error

	return out

def caclulate(exp):
	exp = exp.replace('/', '//')
	if '**' in exp:
		exit(1)
	try:
		value = eval(exp)
		return value
	except:
		exit(1)