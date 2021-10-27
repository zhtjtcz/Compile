from values import *
import lexical.laxer
import tool
import syntactic.analyze
from syntactic.analyze import dfs

def main():
	input = inputfile.read() + '\n'
	input = tool.remove(input)
	lexer = lexical.laxer.getLexer()
	result = syntactic.analyze.getAnalyzer(input, lexer)
	print('declare i32 @getint()\ndeclare void @putint(i32)', file = outputFile)
	# result.dfs_test(result)
	dfs(result)

if __name__ == "__main__":
	main()