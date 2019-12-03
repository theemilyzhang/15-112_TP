from mathFunctions import *

class Board(object):
    def __init__(self, appWidth, appHeight):
        self.topMargin = 20
        self.appWidth = appWidth
        self.appHeight = appHeight
        self.startY = 0
        self.endY = self.appHeight

        #for path method:
        #self.size = 20
        #self.startRow = 4
        #self.grid = self.createPath(self.startRow, [ ([None] * self.size) for row in range(self.size) ])

    def getDirectDxDy(self, bx, by):
        endX = self.appWidth
        endY = self.endY
        distance = getDistance(bx, by, endX, endY)
        deltaX = endX - bx
        deltaY = by - endY #diff order bc y increases while going down
        dx = deltaX/distance
        dy = deltaY/distance
        return dx, dy



    def createPath(self, startRow, startGrid):
        #TODO use backtracking + random to create length n path from left to right starting at startRow

        #currently hardcoded path:
        for i in range(9):
            startGrid[4][i] = (1, 0)
        for i in range(3):
            startGrid[4-i][9] = (0, -1)
        for i in range(11):
            startGrid[1][9+i] = (1, 0)

        return startGrid

    def canPlaceTowerHere(self, x, y, tower):
        tower.halfHeight, tower.halfWidth
        #TODO complete this lol
        pass