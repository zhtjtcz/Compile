import sys
from values import *
import lexical.laxer
import lexical.tool

def main():
	input = ''
	if LOCAL:
		inputfile = open('test.in', 'r')
		input = inputfile.read()
		outputFile = open('test.out', 'w')
	else:
		inputfile = open(sys.argv[1], 'r')
		input = inputfile.read()
		outputFile = open(sys.argv[2], 'w')
	input = lexical.tool.remove(input)
	tokens = lexical.getTokens(input, outputFile)
	
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