import Balloon
import Tower
from mathFunctions import *
import random

class Player(object):
    def __init__(self):
        self.hp = 20
        self.coins = 150
        self.towers = []
        self.bullets = []
        self.cacti = []
        self.placingTower = None
        self.placingCactus = None
        self.illegallyPlacedItem = False
        self.cantAfford = False

        self.offBalloons = self.createBalloons()
        self.onBalloons = []

    def createBalloons(self, difficulty="easy"):
        balloons = []
        balloons.append(Balloon.DisappearingBalloon())
        maxScore = 75
        score = 0
        if difficulty == "hard":
            maxScore = 125
            balloons.append(Balloon.Blimp())

        #indexes:
        #0: Balloon
        #1: BlueBalloon
        #2: GreenBalloon
        #3: YellowBalloon
        #4: PinkBalloon
        #5: DisappearingBalloon
        while score < maxScore:
            index = random.randint(0, 5)
            if index == 0:
                balloons.append(Balloon.Balloon())
            elif index == 1:
                balloons.append(Balloon.BlueBalloon())
            elif index == 2:
                balloons.append(Balloon.GreenBalloon())
            elif index == 3:
                balloons.append(Balloon.YellowBalloon())
            elif index == 4:
                balloons.append(Balloon.PinkBalloon())
            elif index == 5:
                balloons.append(Balloon.DisappearingBalloon())
            if index == 5:
                score += 3
            else:
                score += (index+1)

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



