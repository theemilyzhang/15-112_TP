from mathFunctions import *
import math


class Balloon(object):
    def __init__(self, speed=5, hp=1, color="red"):
        self.speed = speed
        self.hp = hp
        self.color = color
        self.position = (0, 0) #in pixels, aka starts top-left
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
            if restriction[0] > restriction[1]:
                # this "passes go", so to speak, so we want to logically break it up into two restrictions that don't "pass go"
                r1 = (0, restriction[1])
                r2 = (restriction[0], 2 * math.pi)

                index = 0
                while index < len(brange):
                    curTuple = brange[index]  # copy, not a reference
                    if (curTuple[0] <= r1[0] <= curTuple[1] and curTuple[0] <= r1[1] <= curTuple[1]):
                        # if both ends of restriction w/in curTuple, create 2 new restriction tuples
                        brange[index] = (curTuple[0], r1[0])
                        newTuple = (r1[1], curTuple[1])
                        brange.insert(index + 1, newTuple)
                        index += 2
                    elif (r1[0] <= curTuple[0] <= r1[1] and r1[0] <= curTuple[1] <= r1[1]):
                        # if the restriction tuple completely envelops the current tuple, just get rid of the current tuple
                        brange.pop(index)
                    elif (curTuple[0] <= r1[0] <= curTuple[1]):
                        brange[index] = (curTuple[0], r1[0])
                        index += 1
                    elif (curTuple[0] <= r1[1] <= curTuple[1]):
                        brange[index] = (r1[1], curTuple[1])
                        index += 1
                    else:
                        index += 1

                index = 0
                while index < len(brange):
                    curTuple = brange[index]  # copy, not a reference
                    if (curTuple[0] <= r2[0] <= curTuple[1] and curTuple[0] <= r2[1] <= curTuple[1]):
                        # if both ends of restriction w/in curTuple, create 2 new restriction tuples
                        brange[index] = (curTuple[0], r2[0])
                        newTuple = (r2[1], curTuple[1])
                        brange.insert(index + 1, newTuple)
                        index += 2
                    elif (r2[0] <= curTuple[0] <= r2[1] and r2[0] <= curTuple[1] <= r2[1]):
                        # if the restriction tuple completely envelops the current tuple, just get rid of the current tuple
                        brange.pop(index)
                    elif (curTuple[0] <= r2[0] <= curTuple[1]):
                        brange[index] = (curTuple[0], r2[0])
                        index += 1
                    elif (curTuple[0] <= r2[1] <= curTuple[1]):
                        brange[index] = (r2[1], curTuple[1])
                        index += 1
                    else:
                        index += 1
            else:
                index = 0
                while index < len(brange):
                    curTuple = brange[index]  # copy, not a reference
                    if (curTuple[0] <= restriction[0] <= curTuple[1] and curTuple[0] <= restriction[1] <= curTuple[1]):
                        # if both ends of restriction w/in curTuple, create 2 new restriction tuples
                        brange[index] = (curTuple[0], restriction[0])
                        newTuple = (restriction[1], curTuple[1])
                        brange.insert(index + 1, newTuple)
                        index += 2
                    elif (restriction[0] <= curTuple[0] <= restriction[1] and restriction[0] <= curTuple[1] <= restriction[1]):
                        # if the restriction tuple completely envelops the current tuple, just get rid of the current tuple
                        brange.pop(index)
                    elif (curTuple[0] <= restriction[0] <= curTuple[1]):
                        brange[index] = (curTuple[0], restriction[0])
                        index += 1
                    elif (curTuple[0] <= restriction[1] <= curTuple[1]):
                        brange[index] = (restriction[1], curTuple[1])
                        index += 1
                    else:
                        index += 1
        index = 0
        while index < len(brange):
            # get rid of any ranges that are 0 in size
            if brange[index][0] == brange[index][1]:
                brange.pop(index)
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

class FastBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.color = "blue"
        self.speed = 10

class DisappearingBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.color = "purple"
        self.isVisible = True
        self.timeSinceCreation = 0

class ToughBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.color = "pink"
        self.hp = 2

    #TODO: add method that makes it change color if hp = 1