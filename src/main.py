import sys
from values import *
import lexical.laxer
import lexical.tool
import syntactic.analyze

def main():
	input = ''
	if LOCAL:
		inputfile = open('test.in', 'r')
		outputFile = open('test.out', 'w')
	else:
		inputfile = open(sys.argv[1], 'r')
		outputFile = open(sys.argv[2], 'w')
	input = inputfile.read() + '\n'
	input = lexical.tool.remove(input)
	tokens = lexical.laxer.getTokens(input, outputFile)
	# analyzer = syntactic.analyze.Analyzer(tokens, outputFile)
	# analyzer.Ready()
	# analyzer.CompUnit()

if __name__ == "__main__":
	main()