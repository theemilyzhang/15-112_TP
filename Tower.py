from mathFunctions import *
import Balloon
import Bullet

class Tower(object):
    price = 20
    towerRange = 200
    def __init__(self, location):
        self.location = location #tuple
        self.radius = 30
        #TODO check if ^ is accurate
        self.defaultCoolDown = 20
        self.currentCoolDown = self.defaultCoolDown - 1

    def createBulletIfInRange(self, onBalloons):
        #find balloon with max dist traveled that's also in range
        furthestBalloon = None
        for balloon in onBalloons:
            if isinstance(balloon, Balloon.DisappearingBalloon) and not balloon.isVisible:
                continue
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
            return Bullet.Bullet(self.location, dx, dy)
            #return bullet with location of tower and dx dy according to balloon it's shooting at

        return None

class SuperTower(Tower): #faster cooldown, shoots by predicting balloon position
    price = 40
    towerRange = 200
    def __init__(self, location):
        super().__init__(location)
        self.defaultCoolDown = 10
        self.currentCoolDown = self.defaultCoolDown - 1