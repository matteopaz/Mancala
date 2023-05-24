class A:
    def __init__(self, param):
        self.a = param
    
    def new(self):
        return A(self.a + 1)

g = A(1)
print(g.a)
b = g.new()
print(b.a)
