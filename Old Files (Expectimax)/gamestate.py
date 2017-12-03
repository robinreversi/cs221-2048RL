
import collections, random
import numpy as np
import copy

############################################################

class Multi_Game_2048:
    '''
    A wrapper class acting as an intermediate between the individual boards and game.py
    '''

    def __init__(self, n):
        self.n = n
        self.boards = [Game_2048() for _ in range(self.n)]
        self.score = 0
        self.legalMoves = set()

    def updateScore(self):
        self.score = sum(self.boards[k].score for k in range(self.n)) / float(self.n)

    def updateLegalMoves(self):
        legalMoves = self.boards[0].legalMoves
        for k in range(1, self.n):
            legalMoves = set.union(legalMoves, self.boards[k].legalMoves)
        self.legalMoves = legalMoves


    def isEnd(self):
        for k in range(self.n):
            if self.boards[k].isEnd(): return True
        return False

    def getScore(self):
        self.updateScore()
        return self.score

    def getLegalMoves(self):
        self.updateLegalMoves()
        return self.legalMoves

    def swipe(self, swipe):
        for k in range(self.n):
            self.boards[k].swipe(swipe)

    def updateBoard(self):
        for k in range(self.n):
            self.boards[k].placeRandomTile()
            self.boards[k].printScore()
            self.boards[k].printBoard()

############################################################

class Game_2048:
    '''
    Creates a game of 2048.
    Access self.board in the same way as a matrix, i.e. self.board[row][col].
    '''

    def __init__(self):
        self.size = 4
        self.board = np.zeros((self.size, self.size)).astype(int)
        self.score = 0
        self.options = ['a', 's', 'd', 'w']
        self.legalMoves = set()
        self.placeRandomTile()

    '''
    -----------------
    UTILITY FUNCTIONS
    -----------------
    '''

    def printBoard(self):
        print(self.board)
        print('')

    def countZeros(self):
        return np.count_nonzero(self.board == 0)

    '''
    ----------------------
    GAME RUNNING FUNCTIONS
    ----------------------
    ''' 
    def placeRandomTile(self):
        if self.countZeros() == 0: return
        empty_pos = [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row, col] == 0]
        tileval = 4 if random.random() > 0.8 else 2  # assuming a 4:1 distribution ratio
        row, col = random.choice(empty_pos)
        self.board[row, col] = tileval

    def placeTile(self, row, col):
        self.board[row][col] = 2

    def swipeLeft(self):
        for m in range(self.size):
            row = self.board[m, :]
            if sum(row) == 0: continue
            row = row[row != 0]
            rowlist = row.tolist()
            for i in range(row.size - 1):
                if rowlist[i] == rowlist[i + 1]:
                    rowlist[i] *= 2
                    self.score += rowlist[i]
                    rowlist[i + 1] = 0
            newrow = np.array(filter(lambda x: x != 0, rowlist))
            self.board[m, :] = np.concatenate((newrow, np.zeros(self.size - newrow.size)))

    def swipeRight(self):
        for m in range(self.size):
            row = self.board[m, :]
            if sum(row) == 0: continue
            row = row[row != 0]
            rowlist = row.tolist()
            for i in range(row.size - 1, 0, -1):
                if rowlist[i] == rowlist[i - 1]:
                    rowlist[i] *= 2
                    self.score += rowlist[i]
                    rowlist[i - 1] = 0
            newrow = np.array(filter(lambda x: x != 0, rowlist))
            self.board[m, :] = np.concatenate((np.zeros(self.size - newrow.size), newrow))

    def swipeUp(self):
        for m in range(self.size):
            row = self.board[:, m]
            if sum(row) == 0: continue
            row = row[row != 0]
            rowlist = row.tolist()
            for i in range(row.size - 1):
                if rowlist[i] == rowlist[i + 1]:
                    rowlist[i] *= 2
                    self.score += rowlist[i]
                    rowlist[i + 1] = 0
            newrow = np.array(filter(lambda x: x != 0, rowlist))
            self.board[:, m] = np.concatenate((newrow, np.zeros(self.size - newrow.size)))

    def swipeDown(self):
        for m in range(self.size):
            row = self.board[:, m]
            if sum(row) == 0: continue
            row = row[row != 0]
            rowlist = row.tolist()
            for i in range(row.size - 1, 0, -1):
                if rowlist[i] == rowlist[i - 1]:
                    rowlist[i] *= 2
                    self.score += rowlist[i]
                    rowlist[i - 1] = 0
            newrow = np.array(filter(lambda x: x != 0, rowlist))
            self.board[:, m] = np.concatenate((np.zeros(self.size - newrow.size), newrow))


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

    def getHighest(self):
        max = self.board[0,0]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i,j] > max:
                    max = self.board[i,j]
        return max
    # should return a list of new boards
    def generateSuccessor(self, action):
        '''
        pre_action = self.copy()
        if(action == 'a'):
            pre_action.swipeLeft()
        elif(action == 'w'):
            pre_action.swipeUp()
        elif(action == 'd'):
            pre_action.swipeRight()
        else:
            pre_action.swipeDown()
        empty_pos = [(row, col) for row in range(self.size) for col in range(self.size) if pre_action.board[row, col] == 0]
        post_actions = [copy.deepcopy(pre_action) for i in range(len(empty_pos))]
        for i in range(len(post_actions)):
            row, col = empty_pos[i]
            post_actions[i].placeTile(row, col)
        return post_actions
        '''

        post_action = self.copy()
        if(action == 'a'):
            post_action.swipeLeft()
        elif(action == 'w'):
            post_action.swipeUp()
        elif(action == 'd'):
            post_action.swipeRight()
        else:
            post_action.swipeDown()
        for row in range(self.size):
            for col in range(self.size):
                if post_action.board[row, col] == 0 and random.random() > .5:
                    post_action.placeTile(row, col)
        return post_action
        
    def swipe(self, action):
        if(action == 'a'):
            self.swipeLeft()
        elif(action == 'w'):
            self.swipeUp()
        elif(action == 'd'):
            self.swipeRight()
        else:
            self.swipeDown()

    def copy(self):
        return copy.deepcopy(self)

    def getLegalMoves(self):
        self.legalMoves = set()
        if self.countZeros() > 0:
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row, col] == 0:
                        def checkNeighbors(self, row, col):
                            if row - 1 in range(self.size) and self.board[row - 1, col] > 0:
                                self.legalMoves.update('s')
                            if row + 1 in range(self.size) and self.board[row + 1, col] > 0:
                                self.legalMoves.update('w')
                            if col - 1 in range(self.size) and self.board[row, col - 1] > 0:
                                self.legalMoves.update('d')
                            if col + 1 in range(self.size) and self.board[row, col + 1] > 0:
                                self.legalMoves.update('a')
                        checkNeighbors(self, row, col)

        # Check for horizontal matches
        for row in range(self.size):
            for col in range(self.size - 1):
                if self.board[row, col] == self.board[row, col + 1] != 0:
                    self.legalMoves.update('a', 'd')
                    break

        # Check for vertical matches
        for row in range(self.size - 1):
            for col in range(self.size):
                if self.board[row, col] == self.board[row + 1, col] != 0:
                    self.legalMoves.update('s', 'w')
                    break

        return self.legalMoves

    def isEnd(self):
        return len(self.getLegalMoves()) == 0

    def printScore(self):
        print('Current score is %d' % self.score)



############################################################

def playNGames2048(n):
    games = [Game_2048() for _ in range(n)]
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
            score = sum(games[_].score for _ in range(n))
            print('Your score is %2.f!' % (score / float(n)))
            print('Your number of moves is %d' % numMoves)
            return True

    def unionLegalMoves(games, n):
        allLegalMoves = games[0].legalMoves
        for k in range(1, n):
            allLegalMoves = set.union(allLegalMoves, games[k].legalMoves)
        return allLegalMoves

    while 1:
        for k in range(n):
            games[k].placeRandomTile()
            games[k].printBoard()
            games[k].getLegalMoves()
            if checkEndGame(games, k): return

        allLegalMoves = unionLegalMoves(games, n)

        while 1 < 2:
            print("Legal moves are: %s" % ', '.join(move for move in allLegalMoves))
            swipe = games[0].getInput()
            if swipe in allLegalMoves: break
            else: print("Please enter a valid move!")

        for k in range(n):
            games[k].getMove(swipe)

        numMoves += 1


############################################################

#playNGames2048(1)
