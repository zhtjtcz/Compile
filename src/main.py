from values import *
import lexical.laxer
import tool
import syntactic.analyze

def main():
	input = inputfile.read() + '\n'
	try:
		input = tool.remove(input)
		input = input.replace('\n', ' ')
		input = input.replace('\r', ' ')
		print(input, file = outputFile)
		lexer = lexical.laxer.getLexer()
		result = syntactic.analyze.getAnalyzer(input, lexer)
		s = result[4][1][1]
		s = tool.caclulate(s)
		print("define dso_local i32 @main(){\n	ret i32 %d \n}"%s, file = outputFile)
	except:
		exit(1)

if __name__ == "__main__":
	main()