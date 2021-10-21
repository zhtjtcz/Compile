from values import *
import lexical.laxer
import lexical.tool
import syntactic.analyze

def main():
	input = inputfile.read() + '\n'
	input = lexical.tool.remove(input)
	lexer = lexical.laxer.getLexer()
	result = syntactic.analyze.getAnalyzer(input, lexer)
	print(result)


if __name__ == "__main__":
	main()