from mathFunctions import *
import math


class Balloon(object):
    def __init__(self, speed=5, hp=1, color="red"):
        self.speed = speed
        self.hp = hp
        self.color = color
        self.position = (-1, -1) #in pixels, aka starts off-screen
        self.distanceTraveled = 0
        self.radius = 10
        self.coins = 1
        self.angleIncrement = math.pi/16

    def getDirection(self, towers, endX, endY):
        print("in getDirection")
        print("balloon: " + str(self.position[0]) + " " + str(self.position[1]))
        print("end: " + str(endX) + " " + str(endY))
        bx = self.position[0]
        by = self.position[1]
        defaultAngle = getAngle(bx, by, endX, endY)
        brange = []

        for tower in towers:
            tx = tower.location[0]
            ty = tower.location[1]
            print("tower:" + str(tx) + " " + str(ty))
            hypotenuse1 = getDistance(bx, by, tx, ty) #distance between centers, always positive
            oppositeSide1 = tower.radius
            dTheta1 = math.asin(oppositeSide1/hypotenuse1) #positive, 0 to pi

            hypotenuse2 = (hypotenuse1**2 - oppositeSide1**2)**.5
            oppositeSide2 = self.radius
            dTheta2 = math.asin(oppositeSide2/hypotenuse2)

            dTheta = dTheta1 + dTheta2

            angleFromBalloonToTower = getAngle(bx, by, tx, ty)

            restriction = (angleFromBalloonToTower - dTheta, angleFromBalloonToTower + dTheta)
            #make all numbers [0, 2pi)
            if restriction[0] < 0:
                restriction = (restriction[0] + 2*math.pi, restriction[1])
            if restriction[1] < 0:
                restriction = (restriction[0], restriction[1] + 2*math.pi)
            if restriction[0] > 2*math.pi:
                restriction = (restriction[0] - 2*math.pi, restriction[1])
            if restriction[1] > 2*math.pi:
                restriction = (restriction[0], restriction[1] - 2*math.pi)
            self.updateBRange(brange, restriction)

        print(brange)
        return self.getBestDirection(defaultAngle, brange)


    def updateBRange(self, brange, restriction):
        if brange == []:
            if restriction[1] > restriction[0]:
                r1 = (0, restriction[0])
                r2 = (restriction[1], 2*math.pi)
                brange.append(r1)
                brange.append(r2)
            else:
                brange.append((restriction[1], restriction[0]))
        else:
            index = 0
            while index < len(brange):
                curTuple = brange[index] #copy, not a reference
                #if both ends of restriction w/in curTuple, create 2 new restriction tuples
                if (curTuple[0] < restriction[0] < curTuple[1] and
                        curTuple[0] < restriction[1] < curTuple[1]):
                    brange[index] = (curTuple[0], restriction[0])
                    newTuple = (restriction[1], curTuple[1])
                    brange.insert(index+1, newTuple)
                    index += 2
                elif (curTuple[0] < restriction[0] < curTuple[1]):
                    brange[index] = (curTuple[0], restriction[0])
                    index += 1
                elif (curTuple[0] < restriction[1] < curTuple[1]):
                    brange[index] = (restriction[1], curTuple[1])
                    index += 1
                else:
                    index += 1

    def getBestDirection(self, defaultAngle, brange):
        #if brange == [], all directions possible, so auto return default
        if brange == []:
            print(defaultAngle / math.pi * 180)
            return defaultAngle
        #if defaultAngle is legal, return that
        for tuple in brange:
            if tuple[0] <= defaultAngle <= tuple[1]:
                print(defaultAngle / math.pi * 180)
                return defaultAngle
        #otherwise, check for the closest legal angle to defaultAngle
        bestAngle = brange[0][0] #every possible angle will be better than this
        for tuple in brange:
            if getDifferenceBetweenTwoAngles(tuple[0], defaultAngle) < getDifferenceBetweenTwoAngles(bestAngle, defaultAngle):
                bestAngle = tuple[0]
            if getDifferenceBetweenTwoAngles(tuple[1], defaultAngle) < getDifferenceBetweenTwoAngles(bestAngle, defaultAngle):
                bestAngle = tuple[1]
        print(bestAngle / math.pi * 180)
        return bestAngle




    def checkCollision(self, towers, dx, dy):
        #balloon has already been moved
        for tower in towers:
            if self.inTowerRange(tower, dx, dy):
                return True
        return False

    def inTowerRange(self, tower, dx, dy):
        bx = self.location[0]
        by = self.location[1]
        br = self.radius

        tx = tower.location[0]
        ty = tower.location[1]
        tr = tower.towerRange

        bothr = br + tr

        #if balloon is in terminal circle
        balTowCenterDist = getDistance(bx, by, tx, ty)
        if balTowCenterDist <= bothr:
            return True

        return False


    def getWorkingDirection(self, towers, startDx, startDy):
        #loop thru angles until find one that works
        counter = 1
        currentAngle = math.asin(startDy)
        while True:

            newAngle = counter * self.angleIncrement + currentAngle
            dx = math.cos(newAngle)
            dy = math.sin(newAngle)
            if not self.checkCollision(towers, dx, dy):
                return dx, dy

            newAngle = -counter * self.angleIncrement + currentAngle
            dx = math.cos(newAngle)
            dy = math.sin(newAngle)
            if not self.checkCollision(towers, dx, dy):
                return dx, dy

            counter += 1
        pass
