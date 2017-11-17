import collections, random
import numpy as np
############################################################

class Game_2048:
    '''
    Creates a game of 2048.
    Access self.board in the same way as a matrix, i.e. self.board[row][col].
    Suboptimal implementation in some parts - consider converting lists to numpy arrays
    '''

    def __init__(self):
        self.size = 4
        self.board = np.zeros((self.size, self.size))
        self.score = 0
        self.options = ['a', 's', 'd', 'w', 'quit']

    '''
    -----------------
    UTILITY FUNCTIONS
    -----------------
    '''
    def printBoard(self):
        for row in range(self.size):
            print(self.board[row])
        print('')

    def countZeros(self):
        zeros = 0
        for row in self.board:
            zeros += row.count(0)
        return zeros

    '''
    ----------------------
    GAME RUNNING FUNCTIONS
    ----------------------
    ''' 
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

    # The swipes are similar, but slight differences make it convenient to keep them separate.
    # Can gather into one function if really necessary.

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

    '''
    ---------------------
    INTERACTION FUNCTIONS
    ---------------------
    '''
    def getInput(self):
        swipe = ''
        while swipe not in self.options:
            swipe = raw_input("Please enter a, s, d, w, or quit: ")
            print('')
        return swipe

    def getScore(self):
        return self.score

    # definitely need to convert this to checking if legal moves is empty
    def isEnd(self):
        return self.countZeros() == 0

    def generateSuccessor(self, action):
        if(action == 'a'):
            self.swipeLeft()
        elif(action == 'w'):
            self.swipeUp()
        elif(action == 'd'):
            self.swipeRight()
        else:
            self.swipeDown()

    def printScore(self):
        print('Current score is %d' % self.score)

    def getMove(self, swipe):
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

    # TODO: definitely need to convert this to a real get legal actions fn
    # playerIndex will be 0 or 1 depending on whether the player is
    # swiping (0) or the computer is putting a random move
    def getLegalActions(self, playerIndex):
        if(playerIndex == 0):
            return ['a', 'w', 'd', 's']
        else:
            return [(i, j) for i in xrange(self.size) for j in xrange(self.size)\
                    if self.board[i][j] == 0]

############################################################

def playNGames2048(n):
    games = [Game_2048() for _ in xrange(n)]
    numMoves = 0

    print('Welcome to n-2048!')
    print('You will be playing %d concurrent games of 2048!' % n)
    print('Game over when one of the %d boards reaches an end state, i.e. all spaces are filled.' % n)
    print('Score is determined by average score over the %d boards at the end.' % n)
    print('')

    while 1:
        for k in xrange(n):
            if games[k].countZeros() == 0:
                print('Game over at board %d!' % k)
                games[k].printBoard()
                score = sum(games[_].score for _ in xrange(n))
                print('Your score is %2.f!' % (score / float(n)))
                print('Your number of moves is %d' % numMoves)
                return
        for k in xrange(n):
            games[k].placeRandomTile()
            games[k].printBoard()
        swipe = games[0].getInput()
        for k in xrange(n):
            games[k].getMove(swipe)
        numMoves += 1


############################################################

playNGames2048(4)
