import Balloon
import Tower

class Player(object):
    def __init__(self):
        self.hp = 50
        self.coins = 200
        self.towers = []
        self.bullets = []
        self.isPlacingTower = False
        self.isPlacingSuperTower = False

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
        balloons.append(Balloon.DisappearingBalloon)
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
