import collections, random
import numpy as np
import copy
import random as rand

class Game_2048:
    '''
    Creates a game of 2048.
    Access self.board in the same way as a matrix, i.e. self.board[row][col].
    '''
        
    def __init__(self, board, tableL, tableR, scoreTable):
        self.size = 4
        self.board = board
        self.options = ['a', 's', 'd', 'w']
        self.randomize = False
        if tableL != None:
            self.tableL = tableL
            self.tableR = tableR
            self.scoreTable = scoreTable
        else:
            self.initTables()


    '''
    -----------------
    UTILITY FUNCTIONS
    -----------------
    '''
    def initTables(self):
        self.tableL = {}
        self.tableR = {}
        self.scoreTable = {}
        num = self.size << 2
        for a in range(num):
            for b in range(num):
                for c in range(num):
                    for d in range(num):
                        row = np.asarray([a,b,c,d])
                        if sum(row) == 0:
                            self.tableL[0] = 0
                            self.tableR[0] = 0
                            self.scoreTable[0] = 0
                            continue
                        rowL = row[row != 0].copy()
                        rowR = row[row != 0]
                        rowlist = rowL.tolist()
                        for i in range(rowL.size - 1):
                            if rowlist[i] == rowlist[i + 1]:
                                rowlist[i] += 1
                                rowlist[i + 1] = 0
                        newrowL = np.array(filter(lambda x: x != 0, rowlist))
                        newrowL = np.concatenate((newrowL,np.zeros(self.size - newrowL.size))).tolist()
                        newrowL = map(int, newrowL)
                        rowlist = rowR.tolist()
                        for i in range(rowR.size - 1, 0, -1):
                            if rowlist[i] == rowlist[i - 1]:
                                rowlist[i] += 1
                                rowlist[i - 1] = 0
                        newrowR = np.array(filter(lambda x: x != 0, rowlist))
                        newrowR = np.concatenate((np.zeros(self.size - newrowR.size),newrowR)).tolist()
                        newrowR = map(int, newrowR)
                        key = row[0] << 12 | row[1] << 8 | row[2] << 4 | row[3]
                        valL = newrowL[0] << 12 | newrowL[1] << 8 | newrowL[2] << 4 | newrowL[3]
                        valR = newrowR[0] << 12 | newrowR[1] << 8 | newrowR[2] << 4 | newrowR[3]
                        self.tableL[key] = valL
                        self.tableR[key] = valR
                        score = 0
                        for x in range(self.size):
                            val = row[x]
                            score += (val - 1) * (1 << val)
                        self.scoreTable[key] = score
                        
    
    def bitToBoard(self):
        board = np.zeros(self.size ** 2)
        for k in range(self.size ** 2):
            '''
<<<<<<< HEAD
            board[k] = (self.board >> (4 * k)) & 0xF
        board =board.reshape((self.size, self.size))
        '''
            board[k] = 1 << ((self.board >> (4 * k)) & 0xF)
            if board[k] == 1:
                board[k] = 0
        board = board[::-1].reshape((self.size, self.size))
        return board
        
    def printBoard(self):
        print(self.bitToBoard())
        print('')

    def countZeros(self):
        count = 0
        for x in range(self.size ** 2):
            i = 0xF << x
            if i & self.board == 0:
                count+=1
        return count
    
    def emptyPos(self):
        lst = []
        for x in range(self.size ** 2):
            i = 0xF << x
            if i & self.board == 0:
                lst.append(x)
        return lst
    
    def transpose(self,board):
        c1 = board & 0xF0F00F0FF0F00F0F
        c2 = board & 0x0000F0F00000F0F0
        c3 = board & 0x0F0F00000F0F0000
        c = c1 | (c2 << 12) | (c3 >> 12)
        d1 = c & 0xFF00FF0000FF00FF
        d2 = c & 0x00FF00FF00000000
        d3 = c & 0x00000000FF00FF00
        return d1 | (d2 >> 24) | (d3 << 24)
        

    '''
    ----------------------
    GAME RUNNING FUNCTIONS
    ----------------------
    ''' 
    def placeRandomTile(self):
        empty_pos = self.emptyPos()
        if len(empty_pos) == 0: return
    
        if self.randomize:  # turning this off for now
            tileval = 2 if random.random() > 0.8 else 1  # assuming a 4:1 distribution ratio
        else:
            tileval = 2
            
        id = random.choice(empty_pos)
        self.board += tileval << (4 * id)
        

    def placeTile(self, pos):
        self.board = self.board | 1 << (4 * pos)

    def swipeLeft(self):
        row1 = (0xFFFF << 48 & self.board) >> 48
        row2 = (0xFFFF << 32 & self.board) >> 32
        row3 = (0xFFFF << 16 & self.board) >> 16
        row4 = 0xFFFF & self.board
        self.board = self.tableL[row1] << 48 | self.tableL[row2] << 32 | self.tableL[row3] << 16 | self.tableL[row4]

    def swipeRight(self):
        row1 = (0xFFFF << 48 & self.board) >> 48
        row2 = (0xFFFF << 32 & self.board) >> 32
        row3 = (0xFFFF << 16 & self.board) >> 16
        row4 = 0xFFFF & self.board
        self.board = self.tableR[row1] << 48 | self.tableR[row2] << 32 | self.tableR[row3] << 16 | self.tableR[row4]

    def swipeUp(self):
        transpose = self.transpose(self.board)
        row1 = (0xFFFF << 48 & transpose) >> 48
        row2 = (0xFFFF << 32 & transpose) >> 32
        row3 = (0xFFFF << 16 & transpose) >> 16
        row4 = 0xFFFF & transpose
        self.board = self.transpose(self.tableL[row1] << 48 | self.tableL[row2] << 32 | self.tableL[row3] << 16 | self.tableL[row4])

    def swipeDown(self):
        transpose = self.transpose(self.board)
        row1 = (0xFFFF << 48 & transpose) >> 48
        row2 = (0xFFFF << 32 & transpose) >> 32
        row3 = (0xFFFF << 16 & transpose) >> 16
        row4 = 0xFFFF & transpose
        self.board = self.transpose(self.tableR[row1] << 48 | self.tableR[row2] << 32 | self.tableR[row3] << 16 | self.tableR[row4])


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
        '''
        score = 0
        for x in range(self.size ** 2):
            val = ((0xF << x) & self.board) >> x
            if val >= 2:
                score += (val - 1) * (1 << val)
        return score
        '''
        row1 = (0xFFFF << 48 & self.board) >> 48
        row2 = (0xFFFF << 32 & self.board) >> 32
        row3 = (0xFFFF << 16 & self.board) >> 16
        row4 = 0xFFFF & self.board
        return self.scoreTable[row1] + self.scoreTable[row2] + self.scoreTable[row3] + self.scoreTable[row4]

    # should return a list of new boards
    def generateSuccessor(self, action):
        pre_action = Game_2048(self.board, self.tableL, self.tableR, self.scoreTable)
        if(action == 'a'):
            pre_action.swipeLeft()
        elif(action == 'w'):
            pre_action.swipeUp()
        elif(action == 'd'):
            pre_action.swipeRight()
        else:
            pre_action.swipeDown()
        empty_pos = pre_action.emptyPos()
        post_actions = [Game_2048(pre_action.board, pre_action.tableL, pre_action.tableR, pre_action.scoreTable) for i in range(len(empty_pos))]
        for i in range(len(empty_pos)):
            emp = empty_pos[i]
            post_actions[i].placeTile(emp)
        return post_actions

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
        legalmoves = set()
        for action in self.options:
            tempboard = Game_2048
            tempboard.swipe(action)
            if tempboard.board != self.board:
                legalmoves.add(action)
        return legalmoves

    def isEnd(self):
        grid = self.bitToBoard()
        for i in range(self.size):
            for j in range(self.size):
                e = grid[i, j]
                if not e:
                    return False
                if j and e == grid[i, j - 1]:
                    return False
                if i and e == grid[i - 1, j]:
                    return False
        return True

    def printScore(self):
        print('Current score is %d' % self.score)



############################################################

def playNGames2048(n):
    games = [Game_2048.fromNew() for _ in range(n)]
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
            score = sum(games[_].getScore() for _ in range(n))
            print('Your score is %2.f!' % (score / float(n)))
            print('Your number of moves is %d' % numMoves)
            return True

    while 1:
        for k in range(n):
            games[k].placeRandomTile()
            games[k].printBoard()
            if checkEndGame(games, k): return

        allLegalMoves = games[k].options

        while 1 < 2:
            print("Legal moves are: %s" % ', '.join(move for move in allLegalMoves))
            swipe = games[0].getInput()
            if swipe in allLegalMoves: break
            else: print("Please enter a valid move!")

        for k in range(n):
            games[k].swipe(swipe)

        numMoves += 1

#playNGames2048(1)
