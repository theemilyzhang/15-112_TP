from mathFunctions import *

class Board(object):
    def __init__(self, appWidth, appHeight):
        self.topMargin = 20
        self.appWidth = appWidth
        self.appHeight = appHeight
        self.startY = 0
        self.endY = self.appHeight

    def getDirectDxDy(self, bx, by):
        endX = self.appWidth
        endY = self.endY
        distance = getDistance(bx, by, endX, endY)
        deltaX = endX - bx
        deltaY = by - endY #diff order bc y increases while going down
        dx = deltaX/distance
        dy = deltaY/distance
        return dx, dy

