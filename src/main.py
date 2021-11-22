from values import *
import lexical.laxer
import syntactic.analyze
from syntactic.ast import dfs

def main():
	input = inputfile.read() + '\n'
	print(input)
	input  = "const int TAPE_LEN = 65536, BUFFER_LEN = 32768; int       tape[TAPE_LEN], program[BUFFER_LEN], ptr = 0; int main() { int i = 0, len = getint(); while (i < len) { program[i] = getch(); i = i + 1; putch(program[i]); } return 0; }"
	print('declare i32 @getint()', file = outputFile)
	print('declare void @putint(i32)', file = outputFile)
	print('declare i32 @getch()', file = outputFile)
	print('declare void @putch(i32)\n', file = outputFile)
	
	lexer = lexical.laxer.getLexer()
	result = syntactic.analyze.getAnalyzer(input, lexer)
	# result.dfs_test(result, 0, None)
	dfs(result)

if __name__ == "__main__":
	main()