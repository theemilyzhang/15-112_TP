import Balloon
import Tower
from mathFunctions import *

class Player(object):
    def __init__(self):
        self.hp = 2
        self.coins = 200
        self.towers = []
        self.bullets = []
        self.cacti = []
        self.placingTower = None
        self.placingCactus = None
        self.illegallyPlacedItem = False

        self.offBalloons = self.createBalloons()
        self.onBalloons = []

    def createBalloons(self, difficulty="easy"):
        balloons = []

        #TODO make it automatically generate based on level mode

        if difficulty == "easy":
            balloons.append(Balloon.Blimp())
            for i in range(5):
                balloons.append(Balloon.PinkBalloon())
            for i in range(5):
                balloons.append(Balloon.YellowBalloon())
            for i in range(5):
                balloons.append(Balloon.GreenBalloon())
            for i in range(5):
                balloons.append(Balloon.BlueBalloon())
            for i in range(5):
                balloons.append(Balloon.Balloon())
        else:
            balloons.append(Balloon.Blimp())
            for i in range(5):
                balloons.append(Balloon.PinkBalloon())
            for i in range(5):
                balloons.append(Balloon.YellowBalloon())
            for i in range(5):
                balloons.append(Balloon.GreenBalloon())
            for i in range(5):
                balloons.append(Balloon.BlueBalloon())
            for i in range(5):
                balloons.append(Balloon.Balloon())
            pass


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

    def canPlaceItemHere(self, x, y, towerRadius, width, height):
        #return False if:
        #1: overlap with tower
        #2: overlap with cactus
        #3: overlap with balloon
        #4: too close to balloon exit/entrance


        #1
        for tower in self.towers:
            if itemsOverlap(x, y, tower.location[0], tower.location[1], towerRadius, tower.radius):
                return False

        #2
        for cactus in self.cacti:
            if itemsOverlap(x, y, cactus.location[0], cactus.location[1], towerRadius, cactus.radius):
                return False

        #3
        for balloon in self.onBalloons:
            if itemsOverlap(x, y, balloon.position[0], balloon.position[1], towerRadius, balloon.radius):
                return False

        #4
        if getDistance(0, 0, x, y) < 4 * towerRadius:
            return False
        elif getDistance(x, y, width, height) < 4 * towerRadius:
            return False



        return True



