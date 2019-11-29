from mathFunctions import *
import Tower
import math

def getDirection(bx, by, towers, endX, endY):
    defaultAngle = getAngle(bx, by, endX, endY)
    brange = []

    for tower in towers:
        tx = tower.location[0]
        ty = tower.location[1]
        hypotenuse1 = getDistance(bx, by, tx, ty) #distance between centers, always positive
        oppositeSide1 = tower.radius
        try:
            dTheta1 = math.asin(oppositeSide1/hypotenuse1) #positive, 0 to pi
        except:
            print("ok")
        hypotenuse2 = (hypotenuse1**2 - oppositeSide1**2)**.5
        oppositeSide2 = 10
        try:
            dTheta2 = math.asin(oppositeSide2/hypotenuse2)
        except:
            print("ok")
        dTheta = dTheta1 + dTheta2

        angleFromBalloonToTower = getAngle(bx, by, tx, ty)

        restriction = (angleFromBalloonToTower - dTheta, angleFromBalloonToTower + dTheta)
        #make all numbers [0, 2pi)
        if restriction[0] < 0:
            restriction = (restriction[0] + 2*math.pi, restriction[1])
        if restriction[1] < 0:
            restriction = (restriction[0], restriction[1] + 2*math.pi)
        updateBRange(brange, restriction)

    print("brange:")
    print(brange)
    return getBestDirection(defaultAngle, brange)


def updateBRange(brange, restriction):
    if brange == []:
        if restriction[1] > restriction[0]:
            r1 = (0, restriction[0])
            r2 = (restriction[1], 2 * math.pi)
            brange.append(r1)
            brange.append(r2)
        else:
            brange.append((restriction[1], restriction[0]))
    else:
        index = 0
        while index < len(brange):
            curTuple = brange[index]  # copy, not a reference
            # if both ends of restriction w/in curTuple, create 2 new restriction tuples
            if (curTuple[0] < restriction[0] < curTuple[1] and
                    curTuple[0] < restriction[1] < curTuple[1]):
                brange[index] = (curTuple[0], restriction[0])
                newTuple = (restriction[1], curTuple[1])
                brange.insert(index + 1, newTuple)
                index += 2
            elif (curTuple[0] < restriction[0] < curTuple[1]):
                brange[index] = (curTuple[0], restriction[0])
                index += 1
            elif (curTuple[0] < restriction[1] < curTuple[1]):
                brange[index] = (restriction[1], curTuple[1])
                index += 1
            else:
                index += 1


def getBestDirection(defaultAngle, brange):
    # if brange == [], all directions possible, so auto return default
    if brange == []:
        print(defaultAngle / math.pi * 180)
        return defaultAngle
    # if defaultAngle is legal, return that
    for tuple in brange:
        if tuple[0] <= defaultAngle <= tuple[1]:
            print(defaultAngle / math.pi * 180)
            return defaultAngle
    # otherwise, check for the closest legal angle to defaultAngle
    bestAngle = brange[0][0]  # every possible angle will be better than this
    for tuple in brange:
        if getDifferenceBetweenTwoAngles(tuple[0], defaultAngle) < getDifferenceBetweenTwoAngles(bestAngle, defaultAngle):
            bestAngle = tuple[0]
        if getDifferenceBetweenTwoAngles(tuple[1], defaultAngle) < getDifferenceBetweenTwoAngles(bestAngle, defaultAngle):
            bestAngle = tuple[1]
    print(bestAngle / math.pi * 180)
    return bestAngle


towers = []
newTower = Tower.Tower((198, 148))
towers.append(newTower)
newTower = Tower.Tower((233, 117))
towers.append(newTower)
newTower = Tower.Tower((147, 169))
towers.append(newTower)
newTower = Tower.Tower((245, 83))
towers.append(newTower)
print(getDirection(407.8739693663817, 191.53310325342304, towers, 1200, 720))