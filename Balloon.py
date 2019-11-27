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
