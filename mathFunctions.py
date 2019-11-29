import math

def getDistance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**.5

def solveIntersectX(slope1, x1, y1, slope2, x2, y2): #returns x-value of intersection
    #format: slope1(x-x1) + y1 = slope2(x-x2) + y2
    xCoefficient = slope1 - slope2 #left side
    constants = -slope2*(x2) + y2 + slope1*(x1) - y1
    x = constants/xCoefficient
    return x

def getAngle(startX, startY, endX, endY):
    #domain of angle: 0 to pi/2, 3pi/2 to 2pi
    deltaX = endX - startX
    deltaY = startY - endY
    angle = math.atan2(deltaY, deltaX)
    if angle < 0:
        angle += 2*math.pi
    return angle

def getDifferenceBetweenTwoAngles(angle1, angle2):
    if abs(angle1 - angle2) <= math.pi:
        return abs(angle1 - angle2)
    else:
        return 2*math.pi - max(angle1, angle2) + min(angle1, angle2)