import Balloon
import Tower
from mathFunctions import *

class Player(object):
    def __init__(self):
        self.hp = 50
        self.coins = 200
        self.towers = []
        self.bullets = []
        self.isPlacingTower = False
        self.isPlacingSuperTower = False
        self.illegallyPlacedTower = False

        self.offBalloons = self.createBalloons()
        self.onBalloons = []

    def createBalloons(self):
        #TODO make it automatically generate based on level mode
        balloons = []
        """
        for i in range(15):
            balloons.append(Balloon.Balloon())
            balloons.append(Balloon.Balloon())
            balloons.append(Balloon.FastBalloon())
        """
        balloons.append(Balloon.ToughBalloon())
        return balloons

    def moveBalloonOn(self, board):
        #moves a balloon from offBalloons to onBalloons and changes its position to the start of the path
        balloon = self.offBalloons.pop()
        #question: should i be calling a specific Board here^?
        balloon.position = (0, board.startY)
        self.onBalloons.append(balloon)

    def addTower(self, x, y):
        newTower = Tower.Tower((x, y))
        self.towers.append(newTower)

    def canPlaceTowerHere(self, x, y, towerRadius, width, height):
        #return False if overlap with tower or too close to balloon exit/entrance
        for tower in self.towers:
            if self.towersOverlap(x, y, tower.location[0], tower.location[1], towerRadius):
                return False

        if getDistance(0, 0, x, y) < 3*towerRadius:
            return False
        elif getDistance(x, y, width, height) < 3*towerRadius:
            return False

        return True


    def towersOverlap(self, x0, y0, x1, y1, r):
        if getDistance(x0, y0, x1, y1) > 2*r:
            return False
        return True
