class Board(object):
    def __init__(self, appWidth, appHeight):
        self.topMargin = 20
        self.appWidth = appWidth
        self.appHeight = appHeight
        self.size = 20
        self.startRow = 4
        self.grid = self.createPath(self.startRow, [ ([None] * self.size) for row in range(self.size) ])



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

        pass


    #code modified from: http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by app.
        return ((0 <= x <= self.appWidth) and
                (self.topMargin <= y <= self.appHeight))

    def getCell(self, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = self.appWidth
        gridHeight = self.appHeight - self.topMargin
        cellWidth  = gridWidth / self.size
        cellHeight = gridHeight / self.size

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, app.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - self.topMargin) / cellHeight)
        col = int(x / cellWidth)

        return (row, col)

    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = self.appWidth
        gridHeight = self.appHeight - self.topMargin
        cellWidth = gridWidth / self.size
        cellHeight = gridHeight / self.size
        x0 = col * cellWidth
        x1 = x0 + cellWidth
        y0 = self.topMargin + row * cellHeight
        y1 = y0 + cellHeight
        return (x0, y0, x1, y1)