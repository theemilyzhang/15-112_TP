def solveIntersectX(slope1, x1, y1, slope2, x2, y2): #returns x-value of intersection
    #format: slope1(x-x1) + y1 = slope2(x-x2) + y2
    xCoefficient = slope1 - slope2 #left side
    constants = -slope2*(x2) + y2 + slope1*(x1) - y1
    x = constants/xCoefficient
    return x


print(solveIntersectX(3.45, 1, 2, -2, -3.78, -1.5))
