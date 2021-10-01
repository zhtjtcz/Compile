import os
if 'USER' in os.environ.keys():
	LOCAL = (os.environ['USER'] == 'oem')
else:
	LOCAL = False
# ENCODING = 'utf-8'