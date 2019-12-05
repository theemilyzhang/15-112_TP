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
                if self.isFreeze:
                    if balloon.frozenCountdown == 0:
                        balloon.frozenCountdown = balloon.defaultFrozenCountdown
                else:
                    newBalloon = balloon.getWeakerBalloon()
                    onBalloons.remove(balloon)
                    if newBalloon.hp > 0:
                        onBalloons.append(newBalloon)
                return True
        return False

    def collidedWithBalloon(self, balloon):
        bulx1 = self.location[0]
        buly1 = self.location[1]
        bulx0 = bulx1 - (self.dx * self.speed)
        buly0 = buly1 - (self.dy * self.speed)
        bulr = self.radius + 5
        balx = balloon.position[0]
        baly = balloon.position[1]
        balr = balloon.radius + 5
        bothr = bulr + balr

        #if balloon is in terminal circle
        balBulCenterDistCircle = getDistance(balx, baly, bulx1, buly1)
        if balBulCenterDistCircle <= bothr:
            return True

        if self.dx == 0:
            #if balloon is in rectangle
            if abs(bulx1 - balx) < bothr and (buly0 <= baly <= buly1 or buly1 <= baly <= buly0):
                return True
            return False
        elif self.dy == 0:
            #if balloon is in rectangle
            if abs(buly1 - baly) < bothr and (bulx0 <= balx <= bulx1 or bulx1 <= balx <= bulx0):
                return True
            return False
        else:
            dx = bulx1 - bulx0
            dy = buly1 - buly0
            for x in range(20):
                balBulCenterDistCircle = getDistance(balx, baly, bulx1, buly1)
                if balBulCenterDistCircle <= bothr:
                    return True
                bulx0 += dx / 20
                buly0 += dy / 20
            return False