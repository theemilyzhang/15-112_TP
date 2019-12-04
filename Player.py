import Balloon
import Tower
from mathFunctions import *

class Player(object):
    def __init__(self):
        self.hp = 2
        self.coins = 200
        self.towers = []
        self.bullets = []
        self.placingTower = None
        self.illegallyPlacedTower = False

        self.offBalloons = self.createBalloons()
        self.onBalloons = []

    def createBalloons(self):
        #TODO make it automatically generate based on level mode
        balloons = []
        for i in range(5):
            balloons.append(Balloon.PinkBalloon())
        # for i in range(5):
        #     balloons.append(Balloon.YellowBalloon())
        # for i in range(5):
        #     balloons.append(Balloon.GreenBalloon())
        # for i in range(5):
        #     balloons.append(Balloon.BlueBalloon())
        # for i in range(5):
        #     balloons.append(Balloon.Balloon())
        # balloons.append(Balloon.Blimp())
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
        #return False if:
        #1: overlap with tower
        #2: too close to balloon exit/entrance
        #3: overlap with balloon

        #1
        for tower in self.towers:
            if itemsOverlap(x, y, tower.location[0], tower.location[1], towerRadius, towerRadius):
                return False

        #2
        if getDistance(0, 0, x, y) < 4*towerRadius:
            return False
        elif getDistance(x, y, width, height) < 4*towerRadius:
            return False

        #3
        for balloon in self.onBalloons:
            if itemsOverlap(x, y, balloon.position[0], balloon.position[1], towerRadius, balloon.radius):
                return False

        return True



