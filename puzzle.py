from tkinter import *
from tkinter import ttk
from Multi_Game_2048.gameutil import *
from random import *
import gym
from gym import spaces
from gym.utils import seeding
import Multi_Game_2048.Multi_Game_2048_env
import time
import collections,operator
import player
SIZE = 400
GRID_LEN = 4
GRID_PADDING = 5
NUM_BOARDS = 4

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }
FONT = ("Verdana", 20, "bold")

weights1 = [7, 6, 5, 4, 6, 5, 4, 3, 5, 4, 3, 2, 4, 3, 2, 1]
weights2 = [4, 5, 6, 7, 3, 4, 5, 6, 2, 3, 4, 5, 1, 2, 3, 4]
weights3 = [1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6, 4, 5, 6, 7]
weights4 = [4, 3, 2, 1, 5, 4, 3, 2, 6, 5, 4, 3, 7, 6, 5, 4]

util = gameutil()
def evalFn(currentGameState, isEnd, score):
    if isEnd:
        return float('-inf')

    def countZeros(board):
        count = 0
        for x in range(16):
            i = 0xF << (4 * x)
            if i & board == 0:
                count += 1
        return count

    def weightedGrid(board):
        sum1 = 0.0
        sum2 = 0.0
        sum3 = 0.0
        sum4 = 0.0
        for i in range(16):
            val = 1 << ((board >> (4 * i)) & 0xF)
            if val > 1:
                sum1 += weights1[i] * val
                sum2 += weights2[i] * val
                sum3 += weights3[i] * val
                sum4 += weights4[i] * val
        return max(sum1, sum2, sum3, sum4)

    def monotonicity(cGS, k=10.0):

        def monoEval(a, b, e=1.0):
            # if a == b: b += 1  # make [ v ][ v ] the same as [ v ][ v+1 ]
            if a == b: return 2 * k
            return k / (np.log2(b / a) ** e)

        sum = 0.0

        for r in range(4):
            forw = 0.0
            back = 0.0
            for k in range(3):
                forw += monoEval(cGS.board[r, k], cGS.board[r, k + 1])
                back += monoEval(cGS.board[r, k + 1], cGS.board[r, k])
            sum += max(forw, back)

        for c in range(4):
            forw = 0.0
            back = 0.0
            for k in range(3):
                forw += monoEval(cGS.board[k, c], cGS.board[k + 1, c])
                back += monoEval(cGS.board[k + 1, c], cGS.board[k, c])
            sum += max(forw, back)
        return sum

    def openTilePenalty(board, n=5):
        # return util.countZeros(board) - n
        return -((util.countZeros(board) - n) ** 2)

    def smoothness(board):
        sm = 0.0
        for r in range(4):
            for k in range(3):
                sm += abs(util.getTile(board, 4 * r + k) - util.getTile(board, 4 * r + k + 1))

        for c in range(4):
            for k in range(3):
                sm += abs(util.getTile(board, 4 * k + c) - util.getTile(board, 4 * (k + 1) + c))

        return -sm  # penalize high disparity

    eval = 0.0
    eval += score
    eval += weightedGrid(currentGameState)
    # eval += monotonicity(currentGameState, k=10.0)
    # eval += 10 * openTilePenalty(currentGameState)
    eval += smoothness(currentGameState)

    return eval




class GameGrid(Frame):
    def __init__(self,util):
        Frame.__init__(self)
        self.env = gym.make('Multi2048-v0')
        self.env.reset()
        self.env.render()
        self.util = util
        self.grid()
        self.master.title('2048')
        self.grid_cells = []
        self.init_grid()
        self.matrix = [[] for _ in range(NUM_BOARDS)]
        self.update_grid_cells()
        self.agent = player.Player(2, evalFn, self.util, True)
        self.bestScore = 0
        self.mainloop()


    def init_grid(self):
        background1 = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background1.grid(column=0,row=0,padx=5,pady=5)
        s1 = ttk.Separator(background1,orient="vertical")
        grid_cells1 = []
        for i in range(GRID_LEN):
            grid_row = []
            for j in range( GRID_LEN):
                cell = Frame(background1, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            grid_cells1.append(grid_row)
        self.grid_cells.append(grid_cells1)

        background2 = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background2.grid(column=1,row=0,padx=5,pady=5)
        grid_cells2 = []
        for i in range( GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background2, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            grid_cells2.append(grid_row)
        self.grid_cells.append(grid_cells2)

        background3 = Frame(self, bg=BACKGROUND_COLOR_GAME, width= SIZE, height=SIZE)
        background3.grid(column=0,row=1,padx=5,pady=5)
        grid_cells3 = []
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background3, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            grid_cells3.append(grid_row)
        self.grid_cells.append(grid_cells3)

        background4 = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background4.grid(column=1,row=1,padx=5,pady=5)
        grid_cells4 = []
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background4, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            grid_cells4.append(grid_row)
        self.grid_cells.append(grid_cells4)
        v = StringVar()
        v.set("Score: 0")
        scorelbl = Frame(self, width = SIZE, height = 5)
        scorelbl.grid(column=0,row=2)
        Label(master=scorelbl, textvariable=v, fg="#edc22e", justify=CENTER, font=FONT,width = 15, height=1).pack()
        x = StringVar()
        x.set("Best Score: 0")
        scorelbl2 = Frame(self, width=SIZE, height=5)
        scorelbl2.grid(column=1, row=2)
        Label(master=scorelbl2, textvariable=x, fg="#edc22e", justify=CENTER, font=FONT, width=15, height=1).pack()
        self.score = v
        self.best = x

    def update_matrix(self):
        for i in range(NUM_BOARDS):
            self.matrix[i] = self.util.bitToBoard(self.env.boards[i])

    def update_grid_cells(self):
        self.update_matrix()
        for a in range(NUM_BOARDS):
            for i in range(GRID_LEN):
                for j in range(GRID_LEN):
                    new_number = self.matrix[a][i][j]
                    if new_number == 0:
                        self.grid_cells[a][i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    else:
                        self.grid_cells[a][i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                            fg=CELL_COLOR_DICT[new_number])
        temp = "Score: " + str(self.env.getScore())
        self.score.set(temp)
        self.update_idletasks()


    def mainloop(self, n=0):
        while True:
            done = False
            while not done:
                values = collections.defaultdict(float)
                count = collections.defaultdict(float)
                for game in self.env.boards:
                    f, vals = self.agent.getAction(game)
                    for move, score in vals:
                        values[move] += score * util.direness(game)
                        count[move] += 1
                for key in values:
                    values[move] /= count[move]
                maxmov = max(values.items(), key=operator.itemgetter(1))[0]
                new_obs, reward, done, info = self.env.step(maxmov)
                self.update_grid_cells()
                self.update()
            if done:
                curr = self.env.getScore()
                if curr > self.bestScore:
                    self.bestScore = curr
                    self.best.set("Best Score: " + str(curr))
                self.env.reset()
                self.update_grid_cells()
                self.update()

gamegrid = GameGrid(util)

