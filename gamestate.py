import collections, random
import numpy as np
import copy
############################################################

class Game_2048:
    '''
    Creates a game of 2048.
    Access self.board in the same way as a matrix, i.e. self.board[row][col].
    Suboptimal implementation in some parts - consider converting lists to numpy arrays
    '''

    def __init__(self):
        self.size = 4
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)] # np.zeros((self.size, self.size))
        self.score = 0
        self.options = ['a', 's', 'd', 'w', 'quit']
        self.legalMoves = set()

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
        if self.countZeros() == 0: return
        empty_pos = [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row][col] == 0]
        tileval = 2 * random.randint(1, 2)
        row, col = random.sample(empty_pos)
        self.board[row][col] = tileval


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


    def setLegalMoves(self):
        self.legalMoves = set()

        if self.countZeros() > 0:
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == 0:
                        def checkNeighbors(self, row, col):
                            if row - 1 in range(self.size) and self.board[row - 1][col] > 0:
                                self.legalMoves.update('s')
                            if row + 1 in range(self.size) and self.board[row + 1][col] > 0:
                                self.legalMoves.update('w')
                            if col - 1 in range(self.size) and self.board[row][col - 1] > 0:
                                self.legalMoves.update('d')
                            if col + 1 in range(self.size) and self.board[row][col + 1] > 0:
                                self.legalMoves.update('a')
                        checkNeighbors(self, row, col)

        # Check for horizontal matches
        for row in range(self.size):
            for col in range(self.size - 1):
                if self.board[row][col] == self.board[row][col + 1] != 0:
                    self.legalMoves.update('a', 'd')
                    break

        # Check for vertical matches
        for row in range(self.size - 1):
            for col in range(self.size):
                if self.board[row][col] == self.board[row + 1][col] != 0:
                    self.legalMoves.update('s', 'w')
                    break

    def isEnd(self):
        return len(self.legalMoves) == 0

    def generateSuccessor(self, action):
        if action == 'a':
            self.swipeLeft()
        elif action == 'w':
            self.swipeUp()
        elif action == 'd':
            self.swipeRight()
        elif action == 's':
            self.swipeDown()
        else: raise Exception('MoveError: could not generate successor board state')

    def printScore(self):
        print('Current score is %d' % self.score)

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

    def getMove(self, swipe):
        if swipe == 'a':
            self.swipeLeft()
        elif swipe == 's':
            self.swipeDown()
        elif swipe == 'd':
            self.swipeRight()
        elif swipe == 'w':
            self.swipeUp()

    """
    def generateSuccessor(self, agentIndex, action):
        # copy = self.copy(self)
        #if(agentIndex == 0):
            if(action == 'a'):
                copy.swipeLeft()
            elif(action == 'w'):
                copy.swipeUp()
            elif(action == 'd'):
                copy.swipeRight()
            else:
                copy.swipeDown()
        #else:
        #    copy.placeRandomTile()
        #return copy

    #def copy(self):
        #return copy.deepcopy(self)
    """


############################################################

def playNGames2048(n):
    games = [Game_2048() for _ in xrange(n)]
    numMoves = 0

    print('Welcome to n-2048!')
    print('You will be playing %d concurrent games of 2048!' % n)
    print('Game over when one of the %d boards reaches an end state, i.e. all spaces are filled.' % n)
    print('Score is determined by average score over the %d boards at the end.' % n)
    print('')

    def checkEndGame(games, k):
        if games[k].isEnd():
            print('Game over at board %d!' % k)
            games[k].printBoard()
            score = sum(games[_].score for _ in xrange(n))
            print('Your score is %2.f!' % (score / float(n)))
            print('Your number of moves is %d' % numMoves)
            return True

    def unionLegalMoves(games, n):
        allLegalMoves = games[0].legalMoves
        for k in range(1, n):
            allLegalMoves = set.union(allLegalMoves, games[k].legalMoves)
        return allLegalMoves

    while 1:
        for k in xrange(n):
            games[k].placeRandomTile()
            games[k].printBoard()
            games[k].setLegalMoves()
            if checkEndGame(games, k): return

        allLegalMoves = unionLegalMoves(games, n)

        while 1 < 2:
            print("Legal moves are: %s" % ', '.join(move for move in allLegalMoves))
            swipe = games[0].getInput()
            if swipe in allLegalMoves: break
            else: print("Please enter a valid move!")

        for k in xrange(n):
            games[k].getMove(swipe)

        numMoves += 1


############################################################

playNGames2048(4)
