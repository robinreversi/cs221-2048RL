import numpy as np

class gameutil:
    def __init__(self):
        self.size = 4
        self.initTables()


    def getLegalMoves(self, board):
        legalmoves = set()
        for action in range(4):
            new = self.swipe(action, board)
            if self.swipe(action, board) != board:
                legalmoves.add(action)
        return legalmoves


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
                        newrowL = [x for x in rowlist if x != 0]
                        newrowL = np.asarray(newrowL + np.zeros(self.size - len(newrowL)).tolist())
                        newrowL = list(map(int, newrowL))
                        rowlist = rowR.tolist()
                        for i in range(rowR.size - 1, 0, -1):
                            if rowlist[i] == rowlist[i - 1]:
                                rowlist[i] += 1
                                rowlist[i - 1] = 0
                        newrowR = [x for x in rowlist if x != 0]
                        newrowR = np.asarray(np.zeros(self.size - len(newrowR)).tolist() + newrowR)
                        newrowR = list(map(int, newrowR))
                        key = row[0] << 12 | row[1] << 8 | row[2] << 4 | row[3]
                        valL = newrowL[0] << 12 | newrowL[1] << 8 | newrowL[2] << 4 | newrowL[3]
                        valR = newrowR[0] << 12 | newrowR[1] << 8 | newrowR[2] << 4 | newrowR[3]
                        self.tableL[key] = valL
                        self.tableR[key] = valR
                        score = 0
                        for x in range(self.size):
                            val = row[x]
                            if val > 1:
                                score += (val - 1) * (1 << val)
                        self.scoreTable[key] = score

    def getScore(self, board):
        '''
        score = 0
        for x in xrange(self.size ** 2):
            val = ((0xF << x) & self.board) >> x
            if val >= 2:
                score += (val - 1) * (1 << val)
        return score
        '''
        row1 = (0xFFFF << 48 & board) >> 48
        row2 = (0xFFFF << 32 & board) >> 32
        row3 = (0xFFFF << 16 & board) >> 16
        row4 = 0xFFFF & board
        return self.scoreTable[row1] + self.scoreTable[row2] + self.scoreTable[row3] + self.scoreTable[row4]


    # should return a list of new boards
    def generateSuccessor(self, action, board):
        new = self.swipe(action, board)
        empty_pos = self.emptyPos(new)
        post_actions = []
        for i in range(len(empty_pos)):
            emp = empty_pos[i]
            post_actions.append(self.placeTile(emp, new))
        return post_actions


    def placeTile(self, pos, board):
        return board | 1 << (4 * pos)


    def swipe(self, action, board):
        if (action == 3):
            return self.swipeLeft(board)
        elif (action == 0):
            return self.swipeUp(board)
        elif (action == 1):
            return self.swipeRight(board)
        else:
            return self.swipeDown(board)


    def emptyPos(self, board):
        lst = []
        for x in range(16):
            i = 0xF << (4 * x)
            if i & board == 0:
                lst.append(x)
        return lst


    def swipeLeft(self, board):
        row1 = (0xFFFF << 48 & board) >> 48
        row2 = (0xFFFF << 32 & board) >> 32
        row3 = (0xFFFF << 16 & board) >> 16
        row4 = 0xFFFF & board
        return self.tableL[row1] << 48 | self.tableL[row2] << 32 | self.tableL[row3] << 16 | self.tableL[row4]


    def swipeRight(self, board):
        row1 = (0xFFFF << 48 & board) >> 48
        row2 = (0xFFFF << 32 & board) >> 32
        row3 = (0xFFFF << 16 & board) >> 16
        row4 = 0xFFFF & board
        return self.tableR[row1] << 48 | self.tableR[row2] << 32 | self.tableR[row3] << 16 | self.tableR[row4]


    def swipeUp(self, board):
        transpose = self.transpose(board)
        row1 = (0xFFFF << 48 & transpose) >> 48
        row2 = (0xFFFF << 32 & transpose) >> 32
        row3 = (0xFFFF << 16 & transpose) >> 16
        row4 = 0xFFFF & transpose
        return self.transpose(
            self.tableL[row1] << 48 | self.tableL[row2] << 32 | self.tableL[row3] << 16 | self.tableL[row4])


    def swipeDown(self, board):
        transpose = self.transpose(board)
        row1 = (0xFFFF << 48 & transpose) >> 48
        row2 = (0xFFFF << 32 & transpose) >> 32
        row3 = (0xFFFF << 16 & transpose) >> 16
        row4 = 0xFFFF & transpose
        return self.transpose(
            self.tableR[row1] << 48 | self.tableR[row2] << 32 | self.tableR[row3] << 16 | self.tableR[row4])


    def transpose(self, board):
        c1 = board & 0xF0F00F0FF0F00F0F
        c2 = board & 0x0000F0F00000F0F0
        c3 = board & 0x0F0F00000F0F0000
        c = c1 | (c2 << 12) | (c3 >> 12)
        d1 = c & 0xFF00FF0000FF00FF
        d2 = c & 0x00FF00FF00000000
        d3 = c & 0x00000000FF00FF00
        return d1 | (d2 >> 24) | (d3 << 24)


    def isEnd(self, board):
        grid = self.bitToBoard(board)
        for i in range(4):
            for j in range(4):
                e = grid[i, j]
                if not e:
                    return False
                if j and e == grid[i, j - 1]:
                    return False
                if i and e == grid[i - 1, j]:
                    return False
        return True


    def bitToBoard(self, board):
        cboard = np.zeros(16)
        for k in range(16):
            cboard[k] = 1 << ((board >> (4 * k)) & 0xF)
            if cboard[k] == 1:
                cboard[k] = 0
        return cboard[::-1].reshape((4, 4))