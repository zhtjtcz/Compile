import sys
from values import *
import lexical.laxer
import lexical.tool

def main():
	input = ''
	if LOCAL:
		inputfile = open('test.in', 'r')
		input = inputfile.read() + '\n'
		outputFile = open('test.out', 'w')
	else:
		inputfile = open(sys.argv[1], 'r')
		input = inputfile.read() + '\n'
		outputFile = open(sys.argv[2], 'w')
	input = lexical.tool.remove(input)
	symbol = lexical.laxer.getTokens(input, outputFile)

if __name__ == "__main__":
	main()