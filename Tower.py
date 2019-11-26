class Tower(object):
    price = 20
    towerRange = 200
    def __init__(self, location):
        self.location = location #tuple
        self.halfHeight = 30
        self.halfWidth = 10
        self.defaultCoolDown = 20
        self.currentCoolDown = self.defaultCoolDown - 1

        #TODO check if ^ is accurate



    def createBulletIfInRange(self, onBalloons):
        #find balloon with max dist traveled that's also in range
        furthestBalloon = None
        for balloon in onBalloons:
            bx = balloon.position[0]
            by = balloon.position[1]
            tx = self.location[0]
            ty = self.location[1]
            distance = getDistance(tx, ty, bx, by)
            if distance < Tower.towerRange:
                if (furthestBalloon == None):
                    furthestBalloon = balloon
                elif (balloon.distanceTraveled > furthestBalloon.distanceTraveled):
                    furthestBalloon = balloon #never gets to here

        #possible that furthestBalloon is still none
        if furthestBalloon != None:
            deltaX = furthestBalloon.position[0] - self.location[0]
            deltaY = furthestBalloon.position[1] - self.location[1]
            scaleFactor = (deltaX**2 + deltaY**2)**.5
            dx = deltaX/scaleFactor
            dy = deltaY/scaleFactor
            return Bullet(self.location, dx, dy)
            #return bullet with location of tower and dx dy according to balloon it's shooting at

        return None

class Bullet(object):

    def __init__(self, location, dx, dy):
        self.location = location
        self.dx = dx
        self.dy = dy
        self.speed = 50
        self.radius = 2
        self.distanceTraveled = 0
        self.bulletRange = 200


    def checkCollision(self, onBalloons):
        #note: bullet is at new location (already been moved)
        bx = self.location[0]
        by = self.location[1]
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


def getDistance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**.5

def solveIntersectX(slope1, x1, y1, slope2, x2, y2): #returns x-value of intersection
    #format: slope1(x-x1) + y1 = slope2(x-x2) + y2
    xCoefficient = slope1 - slope2 #left side
    constants = -slope2*(x2) + y2 + slope1*(x1) - y1
    x = constants/xCoefficient
    return x
