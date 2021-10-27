from values import *
import lexical.laxer
import tool
import syntactic.analyze

def main():
	input = inputfile.read() + '\n'
	try:
		input = tool.remove(input)
		lexer = lexical.laxer.getLexer()
		result = syntactic.analyze.getAnalyzer(input, lexer)
		result.dfs_test()
	except:
		exit(1)

if __name__ == "__main__":
	main()