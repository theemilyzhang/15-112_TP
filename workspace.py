def solveIntersectX(slope1, x1, y1, slope2, x2, y2): #returns x-value of intersection
    #format: slope1(x-x1) + y1 = slope2(x-x2) + y2
    xCoefficient = slope1 - slope2 #left side
    constants = -slope2*(x2) + y2 + slope1*(x1) - y1
    x = constants/xCoefficient
    return x

def testReturnTuple(x, y):
    return x, y

class Tower(object):
    price = 20
    towerRange = 200
    def __init__(self, location):
        self.location = location #tuple

t = Tower((4,3))

print(t.towerRange)
