class A():
	def __init__(self):
		self.x = {}

a = A()
a.x[1] = 2
b = A()
b.x = a.x.copy()
b.x[2] = 3
print(a.x)
print(b.x)
