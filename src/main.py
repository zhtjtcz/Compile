from values import *
import lexical.laxer
import tool
import syntactic.analyze
from syntactic.ast import dfs

def main():
	input = inputfile.read() + '\n'
	input = tool.remove(input)
	print(input)
	lexer = lexical.laxer.getLexer()
	result = syntactic.analyze.getAnalyzer(input, lexer)
	# result.dfs_test(result, 0, None)
	'''
	print('declare i32 @getint()', file = outputFile)
	print('declare void @putint(i32)', file = outputFile)
	print('declare i32 @getch()', file = outputFile)
	print('declare void @putch(i32)\n', file = outputFile)
	'''
	dfs(result)

if __name__ == "__main__":
	main()