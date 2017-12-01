import collections, random
import numpy as np
import copy
import random as rand

class Game_2048:
    '''
    Creates a game of 2048.
    Access self.board in the same way as a matrix, i.e. self.board[row][col].
    '''
        
    def __init__(self, board, tableL, tableR):
        self.size = 4
        self.board = board
        self.options = ['a', 's', 'd', 'w']
        self.legalMoves = set()
        self.randomize = False
        if tableL != None:
            self.tableL = tableL
            self.tableR = tableR
        else:
            self.initTables
        
    @classmethod
    def fromNew(cls):
        cls(long(0) + 1 << (4 * rand.randint(0,15)), None, None)
        
        
    @classmethod
    def fromOld(cls,board,tableL,tableR):
        cls(board, tableL, tableR)

    '''
    -----------------
    UTILITY FUNCTIONS
    -----------------
    '''
    def initTables(self):
        self.tableL = {}
        self.tableR = {}
        num = self.size << 2
        for a in range(num):
            for b in range(num):
                for c in range(num):
                    for d in range(num):
                        row = np.asarray([a,b,c,d])
                        if sum(row) == 0:
                            self.tableL[0] = 0
                            self.tableR[0] = 0
                            continue
                        rowL = row[row != 0].copy()
                        rowR = row[row != 0]
                        rowlist = rowL.tolist()
                        for i in xrange(row.size - 1):
                            if rowlist[i] == rowlist[i + 1]:
                                rowlist[i] *= 2
                                self.score += rowlist[i]
                                rowlist[i + 1] = 0
                        newrowL = np.array(filter(lambda x: x != 0, rowlist))
                        rowlist = rowR.tolist()
                        for i in xrange(row.size - 1, 0, -1):
                            if rowlist[i] == rowlist[i - 1]:
                                rowlist[i] *= 2
                                self.score += rowlist[i]
                                rowlist[i - 1] = 0
                        newrowR = np.array(filter(lambda x: x != 0, rowlist))
                        key = row[0] << 48 | row[1] << 32 | row[2] << 16 | row[3]
                        valL = newrowL[0] << 48 | newrowL[1] << 32 | newrowL[2] << 16 | newrowL[3]
                        valR = newrowR[0] << 48 | newrowR[1] << 32 | newrowR[2] << 16 | newrowR[3]
                        self.tableL[key] = valL
                        self.tableR[key] = valR
                        
    
    def bitToBoard(self):
        board = np.array(self.size ** 2)
        for k in xrange(self.size ** 2):
            board[k] = (self.board >> (4 * k)) & 0xF
        board.reshape((self.size, self.size))
        return board
        
    def printBoard(self):
        print(self.bitToBoard())
        print('')

    def countZeros(self):
        count = 0
        for x in xrange(self.size ** 2):
            i = 0xF << x
            if i & self.board == 0:
                count+=1
        return count
    
    def emptyPos(self):
        lst = []
        for x in xrange(self.size ** 2):
            i = 0xF << x
            if i & self.board == 0:
                lst.append(x)
        return lst
    
    def transpose(self):
        c1 = self.board & 0xF0F00F0FF0F00F0F
        c2 = self.board & 0x0000F0F00000F0F0
        c3 = self.board & 0x0F0F00000F0F0000
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
        self.board += 1 << (4 * pos)

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
        score = 0
        for x in xrange(self.size ** 2):
            val = ((0xF << x) & self.board) >> x
            if val >= 2:
                score += (val - 1) * (1 << val)
        return score

    # should return a list of new boards
    def generateSuccessor(self, action):
        pre_action = Game_2048.fromOld(self.board, self.tableL, self.tableR)
        if(action == 'a'):
            pre_action.swipeLeft()
        elif(action == 'w'):
            pre_action.swipeUp()
        elif(action == 'd'):
            pre_action.swipeRight()
        else:
            pre_action.swipeDown()
        empty_pos = self.emptyPos()
        post_actions = [Game_2048.fromOld(self.board, self.tableL, self.tableR) for i in xrange(len(empty_pos))]
        for i in range(len(post_actions)):
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
        for action in self.actions:
            tempboard = copy.deepcopy(self)
            tempboard.swipe(action)
            if tempboard.board != self.board:
                legalmoves.add(action)
        return legalmoves

    def isEnd(self):
        return len(self.getLegalMoves()) == 0

    def printScore(self):
        print('Current score is %d' % self.score)



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
            games[k].getLegalMoves()
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
