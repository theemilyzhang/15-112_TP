import Balloon
import Board
import Tower

class Player(object):
    def __init__(self):
        self.hp = 50
        self.coins = 20
        self.towers = []
        self.bullets = []
        self.isPlacingTower = False

        self.offBalloons = self.createBalloons()
        self.onBalloons = []



    def createBalloons(self):
        #TODO make it automatically generate based on some user input
        balloons = []
        for i in range(30):
            balloons.append(Balloon.Balloon())

        return balloons

    def moveBalloonOn(self, board):
        #moves a balloon from offBalloons to onBalloons and changes its position to the start of the path
        balloon = self.offBalloons.pop()
        y0 = board.getCellBounds(board.startRow, 0)[1]
        y1 = board.getCellBounds(board.startRow, 0)[3]
        #question: should i be calling a specific Board here^?
        yStart = (y0 + y1)//2
        balloon.position = (0, yStart)
        self.onBalloons.append(balloon)

    def addTower(self, x, y):
        newTower = Tower.Tower((x, y))
        self.towers.append(newTower)



