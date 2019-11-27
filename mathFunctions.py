
def getDistance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**.5

def solveIntersectX(slope1, x1, y1, slope2, x2, y2): #returns x-value of intersection
    #format: slope1(x-x1) + y1 = slope2(x-x2) + y2
    xCoefficient = slope1 - slope2 #left side
    constants = -slope2*(x2) + y2 + slope1*(x1) - y1
    x = constants/xCoefficient
    return x