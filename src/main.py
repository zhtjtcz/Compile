from values import *
import lexical.laxer
import tool
import syntactic.analyze

def main():
	input = inputfile.read() + '\n'
	input = tool.remove(input)
	lexer = lexical.laxer.getLexer()
	result = syntactic.analyze.getAnalyzer(input, lexer)
	result.dfs_test()

if __name__ == "__main__":
	main()