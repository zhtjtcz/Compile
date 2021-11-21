import os
import sys
import platform

LOCAL = False
if platform.system()=='Windows':
	LOCAL = True
elif 'USER' in os.environ.keys():
	LOCAL = (os.environ['USER'] == 'oem')

if LOCAL:
	inputfile = open('a.c', 'r')
	outputFile = open('test.ll', 'w')
else:
	inputfile = open(sys.argv[1], 'r')
	outputFile = open(sys.argv[2], 'w')