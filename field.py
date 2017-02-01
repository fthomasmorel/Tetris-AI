import copy

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[0]*self.width]*self.height

    def size(self):
        return self.width, self.height

    def updateField(self, field):
        self.field = field

    @staticmethod
    def check_collision(field, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and field[ cy + off_y ][ cx + off_x ]:
                        return True
                except IndexError:
                    return True
        return False

    def projectPieceDown(self, piece, offsetX, workingPieceIndex):
        if offsetX+len(piece[0]) > self.width or offsetX < 0:
            return None
        #result = copy.deepcopy(self)
        offsetY = self.height
        for y in range(0, self.height):
            if Field.check_collision(self.field, piece, (offsetX, y)):
                offsetY = y
                break
        for x in range(0, len(piece[0])):
            for y in range(0, len(piece)):
                value = piece[y][x]
                if value > 0:
                    self.field[offsetY-1+y][offsetX+x] = -workingPieceIndex
        return self

    def undo(self, workingPieceIndex):
        self.field = [[0 if el == -workingPieceIndex else el for el in row] for row in self.field]

    def heightForColumn(self, column):
        width, height = self.size()
        for i in range(0, height):
            if self.field[i][column] != 0:
                return height-i
        return 0

    def heights(self):
        result = []
        width, height = self.size()
        for i in range(0, width):
            result.append(self.heightForColumn(i))
        return result

    def numberOfHoleInColumn(self, column):
        result = 0
        maxHeight = self.heightForColumn(column)
        for height, line in enumerate(reversed(self.field)):
            if height > maxHeight: break
            if line[column] == 0 and height < maxHeight:
                result+=1
        return result

    def numberOfHoleInRow(self, line):
        result = 0
        for index, value in enumerate(self.field[self.height-1-line]):
            if value == 0 and self.heightForColumn(index) > line:
                result += 1
        return result

    ################################################
    #                   HEURISTICS                 #
    ################################################

    def heuristics(self):
        heights = self.heights()
        maxColumn = self.maxHeightColumns(heights)
        return heights + [self.aggregateHeight(heights)] + self.numberOfHoles(heights) + self.bumpinesses(heights) + [self.completLine(), self.maxPitDepth(heights), self.maxHeightColumns(heights), self.minHeightColumns(heights)]

    def aggregateHeight(self, heights):
        result = sum(heights)
        return result

    def completLine(self):
        result = 0
        width, height = self.size()
        for i in range (0, height) :
            if 0 not in self.field[i]:
                result+=1
        return result

    def bumpinesses(self, heights):
        result = []
        for i in range(0, len(heights)-1):
            result.append(abs(heights[i]-heights[i+1]))
        return result

    def numberOfHoles(self, heights):
        results = []
        width, height = self.size()
        for j in range(0, width) :
            result = 0
            for i in range (0, height) :
                if self.field[i][j] == 0 and height-i < heights[j]:
                    result+=1
            results.append(result)
        return results

    def maxHeightColumns(self, heights):
        return max(heights)

    def minHeightColumns(self, heights):
        return min(heights)

    def maximumHoleHeight(self, heights):
        if self.numberOfHole(heights) == 0:
            return 0
        else:
            maxHeight = 0
            for height, line in enumerate(reversed(self.field)):
                if sum(line) == 0: break
                if self.numberOfHoleInRow(height) > 0:
                    maxHeight = height
            return maxHeight

    def rowsWithHoles(self, maxColumn):
        result = 0
        for line in range(0, maxColumn):
            if self.numberOfHoleInRow(line) > 0:
                result += 1
        return result

    def maxPitDepth(self, heights):
        return max(heights)-min(heights)



    @staticmethod
    def __offsetPiece(piecePositions, offset):
        piece = copy.deepcopy(piecePositions)
        for pos in piece:
            pos[0] += offset[0]
            pos[1] += offset[1]

        return piece

    def __checkIfPieceFits(self, piecePositions):
        for x,y in piecePositions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.field[y][x] >= 1:
                    return False
            else:
                return False
        return True

    def fitPiece(self, piecePositions, offset=None):
        if offset:
            piece = self.__offsetPiece(piecePositions, offset)
        else:
            piece = piecePositions

        field = copy.deepcopy(self.field)
        if self.__checkIfPieceFits(piece):
            for x,y in piece:
                field[y][x] = 1

            return field
        else:
            return None
