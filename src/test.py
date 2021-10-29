class A():
	def __init__(self):
		self.x = 1

def f(x : A):
	x.x = 2

a = A()
f(a)
print(a.x)