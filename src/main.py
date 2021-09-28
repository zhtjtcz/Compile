import sys
from values import *
from token import Token

def Main():
	input = ''
	if LOCAL:
		inputfile = open('test.in', 'r')
		input = inputfile.read()
	lex = Token(input)
	while lex.IsEnd() != False:
		print(lex.GetToken())

if __name__ == "__main__":
	Main()