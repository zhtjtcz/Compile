from values import *
import lexical.laxer
import syntactic.analyze
from syntactic.ast import dfs

def main():
	input = inputfile.read() + '\n'
	print(input)
	print('declare i32 @getint()', file = outputFile)
	print('declare void @putint(i32)', file = outputFile)
	print('declare i32 @getch()', file = outputFile)
	print('declare void @putch(i32)', file = outputFile)
	print('declare i32 @getarray(i32*)', file = outputFile)
	print('declare void @putarray(i32, i32*)\n', file = outputFile)
	
	lexer = lexical.laxer.getLexer()
	result = syntactic.analyze.getAnalyzer(input, lexer)
	dfs(result)

if __name__ == "__main__":
	main()