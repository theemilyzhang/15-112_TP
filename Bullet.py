from mathFunctions import *

class Bullet(object):

    def __init__(self, location, dx, dy):
        self.location = location
        self.dx = dx
        self.dy = dy
        self.speed = 50
        self.radius = 2
        self.distanceTraveled = 0
        self.bulletRange = 200
        self.isFreeze = False


    def checkCollision(self, onBalloons):
        #note: bullet is at new location (already been moved)
        for balloon in onBalloons:
            if self.collidedWithBalloon(balloon):
                #decrement balloon hp, then remove if dead
                balloon.hp -= 1
                if balloon.hp <= 0:
                    onBalloons.remove(balloon)
                return True
        return False

    def collidedWithBalloon(self, balloon):
        bulx1 = self.location[0]
        buly1 = self.location[1]
        bulx0 = bulx1 - (self.dx * self.speed)
        buly0 = buly1 - (self.dy * self.speed)
        bulr = self.radius

        if self.dx == 0:
            # todo write logic for when the slope is essentially infinite
        else:
            bulSlope = -self.dy/self.dx

            balx = balloon.position[0]
            baly = balloon.position[1]
            balr = balloon.radius

            bothr = bulr + balr

            #if balloon is in terminal circle
            balBulCenterDistCircle = getDistance(balx, baly, bulx1, buly1)
            if balBulCenterDistCircle <= bothr:
                return True

            #if balloon is in rectangle
            perpSlope = -1 * (1/bulSlope)
            intersectX = solveIntersectX(bulSlope, bulx1, buly1, perpSlope, balx, baly)
            intersectY = bulSlope * (intersectX - bulx0) + buly0
            balBulCenterDistRectangle = getDistance(balx, baly, intersectX, intersectY)

            if (min(bulx0, bulx1) <= intersectX <= max(bulx0, bulx1) and
                    min(buly0, buly1) <= intersectY <= max(buly0, buly1) and
                    balBulCenterDistRectangle <= bothr):
                return True

            return False