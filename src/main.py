import sys
from values import *
from laxer import Laxer
import tool

def main():
	input = ''
	if LOCAL:
		inputfile = open('test.in', 'r')
		input = inputfile.read()
	else:
		inputfile = open(sys.argv[1], 'r')
		input = inputfile.read()
	input = tool.remove(input)
	# print(input)
	'''
	lex = Laxer(input)
	if LOCAL:
		f = open('test.out', 'w')

	while lex.isEnd() == False:
		token = lex.getToken()
		if token == '':
			break
		if LOCAL:
			print(token, file = f)
		else:
			print(token)
		if token.lexeme == 'Err':
			break
	'''

if __name__ == "__main__":
	main()