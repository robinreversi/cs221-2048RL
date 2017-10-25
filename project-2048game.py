import collections, random

############################################################

class game_2048:
    '''
    Creates a game of 2048.
    Access self.board in the same way as a matrix, i.e. self.board[row][col].
    Suboptimal implementation in some parts - consider converting lists to numpy arrays
    '''

    def __init__(self):
        self.size = 4
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.options = ['a', 's', 'd', 'w', 'quit']

    def printBoard(self):
        for row in range(self.size):
            print(self.board[row])
        print('')

    def countZeros(self):
        zeros = 0
        for row in self.board:
            zeros += row.count(0)
        return zeros

    def placeRandomTile(self):
        rand = random.randint(1, self.countZeros())
        tileVal = 2 * random.randint(1, 2)
        count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    count += 1
                    if count == rand:
                        self.board[row][col] = tileVal
                        return

    def swipeLeft(self):
        for row in range(self.size):
            if sum(self.board[row]) == 0: continue
            newRow = filter(lambda x: x != 0, self.board[row])
            for x in range(len(newRow) - 1):
                if newRow[x] == newRow[x + 1]:
                    newRow[x + 1] *= 2
                    self.score += newRow[x + 1]
                    del newRow[x]
                    break
            while len(newRow) < self.size: newRow.append(0)
            self.board[row] = newRow

    # The swipes are similar, but slight differences make it convenient to keep them separate.
    # Can gather into one function if necessary.
    def swipeRight(self):
        for row in range(self.size):
            if sum(self.board[row]) == 0: continue
            newRow = filter(lambda x: x != 0, self.board[row])
            for _ in range(len(newRow) - 1):
                x = len(newRow) - _ - 1
                if newRow[x] == newRow[x - 1]:
                    newRow[x - 1] *= 2
                    self.score += newRow[x - 1]
                    del newRow[x]
                    break
            while len(newRow) < self.size: newRow = [0] + newRow
            self.board[row] = newRow

    def swipeUp(self):
        for col in range(self.size):
            column = [self.board[row][col] for row in range(self.size)]
            if sum(column) == 0: continue
            newCol = filter(lambda x: x != 0, column)
            for x in range(len(newCol) - 1):
                if newCol[x] == newCol[x + 1]:
                    newCol[x + 1] *= 2
                    self.score += newCol[x + 1]
                    del newCol[x]
                    break
            while len(newCol) < self.size: newCol.append(0)
            for row in range(self.size):
                self.board[row][col] = newCol[row]

    def swipeDown(self):
        for col in range(self.size):
            column = [self.board[row][col] for row in range(self.size)]
            if sum(column) == 0: continue
            newCol = filter(lambda x: x != 0, column)
            for _ in range(len(newCol) - 1):
                x = len(newCol) - _ - 1
                if newCol[x] == newCol[x - 1]:
                    newCol[x - 1] *= 2
                    self.score += newCol[x - 1]
                    del newCol[x]
                    break
            while len(newCol) < self.size: newCol = [0] + newCol
            for row in range(self.size):
                self.board[row][col] = newCol[row]

    def getInput(self):
        swipe = ''
        while swipe not in self.options:
            swipe = raw_input("Please enter a, s, d, w, or quit: ")
        return swipe

    def getMove(self):
        swipe = self.getInput()
        if swipe == 'a':
            self.swipeLeft()
        elif swipe == 's':
            self.swipeDown()
        elif swipe == 'd':
            self.swipeRight()
        elif swipe == 'w':
            self.swipeUp()
        else:
            return

    def printScore(self):
        print('Current score is %d' % self.score)

############################################################

def play2048():
    game = game_2048()

    while 1:
        if game.countZeros() == 0:
            print("Game over!")
        game.printScore()
        game.placeRandomTile()
        game.printBoard()
        game.getMove()

############################################################

play2048()