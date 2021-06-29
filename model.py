class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[0] * self.width] * self.height

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
                    if cell and field[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False

    def projectPieceDown(self, piece, offsetX, workingPieceIndex):
        if offsetX + len(piece[0]) > self.width or offsetX < 0:
            return None
        offsetY = self.height
        for y in range(0, self.height):
            if Field.check_collision(self.field, piece, (offsetX, y)):
                offsetY = y
                break
        for x in range(0, len(piece[0])):
            for y in range(0, len(piece)):
                value = piece[y][x]
                if value > 0:
                    self.field[offsetY - 1 + y][offsetX + x] = -workingPieceIndex
        return self

    def undo(self, workingPieceIndex):
        self.field = [[0 if el == -workingPieceIndex else el for el in row] for row in self.field]

    def heightForColumn(self, column):
        width, height = self.size()
        for i in range(0, height):
            if self.field[i][column] != 0:
                return height - i
        return 0

    def heights(self):
        result = []
        width, height = self.size()
        for i in range(0, width):
            result.append(self.heightForColumn(i))
        return result

    def heuristics(self):
        heights = self.heights()
        list = []
        list.append(self.aggregateHeight(heights))
        list.append(self.completedLine())
        list.append(self.numberOfHoles(heights))
        list.append(self.bumpinesses(heights))
        return list

    def aggregateHeight(self, heights):
        result = sum(heights)
        return result

    def completedLine(self):
        result = 0
        width, height = self.size()
        for i in range(0, height):
            if 0 not in self.field[i]:
                result += 1
        return result

    def bumpinesses(self, heights):
        result = 0
        for i in range(0, len(heights) - 1):
            result += abs(heights[i] - heights[i + 1])
        return result

    def numberOfHoles(self, heights):
        total = 0
        width, height = self.size()
        for j in range(0, width):
            result = 0
            for i in range(0, height):
                if self.field[i][j] == 0 and height - i < heights[j]:
                    result += 1
            total += result
        return total
