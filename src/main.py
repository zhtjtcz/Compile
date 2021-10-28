from values import *
import lexical.laxer
import tool
import syntactic.analyze
from syntactic.analyze import dfs

def main():
	try:
		input = inputfile.read() + '\n'
		input = tool.remove(input)
		lexer = lexical.laxer.getLexer()
		result = syntactic.analyze.getAnalyzer(input, lexer)
		# result.dfs_test(result, 0, None)
		dfs(result)
	except:
		exit(1)

if __name__ == "__main__":
	main()