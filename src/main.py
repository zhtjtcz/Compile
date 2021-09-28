import sys
from values import *
from laxer import Laxer

def main():
	input = ''
	if LOCAL:
		inputfile = open('test.in', 'r')
		input = inputfile.read()
	else:
		pass
	
	lex = Laxer(input)
	f = open('test.out', 'w')
	while lex.isEnd() == False:
		token = lex.getToken()
		print(token, file = f)
		if token.lexeme == 'Err':
			break

if __name__ == "__main__":
	main()