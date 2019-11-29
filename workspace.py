class A(object):
    def __init__(self):
        self.x = "A"
        self.num = 5

class B(A):
    def __init__(self):
        super().__init__()
        self.num = 6

thing = B()
print (thing.x)
print (thing.num)
