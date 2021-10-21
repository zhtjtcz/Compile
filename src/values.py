import os
import sys

if 'USER' in os.environ.keys():
	LOCAL = (os.environ['USER'] == 'oem')
else:
	LOCAL = False
# ENCODING = 'utf-8'

if LOCAL:
	inputfile = open('test.in', 'r')
	outputFile = open('test.out', 'w')
else:
	inputfile = open(sys.argv[1], 'r')
	outputFile = open(sys.argv[2], 'w')