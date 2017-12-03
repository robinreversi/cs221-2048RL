import gym
from gym import spaces
from gym.utils import seeding

import numpy as np
import random

import itertools
import logging
from six import StringIO
import sys

'''
======================
   MultiGame2048Env
======================
'''

class MultiGame2048Env(gym.Env):
    '''
    A wrapper class acting as an intermediate between the individual boards and game.py
    '''
    
    def __init__(self):
        self.n = 2
        self.boards = [Game_2048() for _ in xrange(self.n)]
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.MultiDiscrete([range(16) for _ in (self.n * 16)])
        self.score = 0
        self.legalMoves = set()
        self._seed()
        self._reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        """Perform one step of the game. This involves moving and adding a new tile."""
        reward = 0
        done = False
        observation = np.ndarray()
        for k in xrange(self.n):
            prevScore = self.boards[k].getScore()
            self.boards[k].swipe(action)
            reward += self.boards[k].getScore() - prevScore
            if self.boards[k].isEnd(): done = True
            observation = np.concatenate(observation,self.boards[k].board.flatten())
        return observation, reward, done, dict()
    
    def _reset(self):
        """Reset the board to begin a new game. Places two random tiles on the board."""
        self.boards = [Game_2048() for _ in xrange(self.n)]
        self.score = 0
        self.legalMoves = set()
    
    def _render(self, mode='human', close=False):
        if close:
            return
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        s = 'Score: {}\n'.format(self.score)
        for board in self.boards:
            s += "{}\n".format(board)
        outfile.write(s)
        return outfile
    
    ############### Non-OpenAI Gym functions ###############
    
    def updateScore(self):
        self.score = sum(self.boards[k].score for k in xrange(self.n)) / float(self.n)

    def updateLegalMoves(self):
        legalMoves = self.boards[0].legalMoves
        for k in xrange(1, self.n):
            legalMoves = set.union(legalMoves, self.boards[k].legalMoves)
        self.legalMoves = legalMoves

    def isEnd(self):
        for k in xrange(self.n):
            if self.boards[k].isEnd(): return True
        return False

    def getScore(self):
        self.updateScore()
        return self.score

    def getLegalMoves(self):
        self.updateLegalMoves()
        return self.legalMoves

    def swipe(self, swipe):
        for k in xrange(self.n):
            self.boards[k].swipe(swipe)

    def updateBoard(self):
        for k in xrange(self.n):
            self.boards[k].placeRandomTile()
            self.boards[k].printScore()
            self.boards[k].printBoard()

'''
======================
       Game_2048
======================
'''

class Game_2048:
    '''
    Creates a game of 2048.
    Access self.board in the same way as a matrix, i.e. self.board[row][col].
    '''

    def __init__(self):
        self.size = 4
        self.board = np.zeros((self.size, self.size))
        self.score = 0
        self.options = range(0, 4)
        self.legalMoves = set()
        self.placeRandomTile()

    '''
    -----------------
    UTILITY FUNCTIONS
    -----------------
    '''

    def placeRandomTile(self):
        if self.countZeros() == 0: return
        empty_pos = [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row, col] == 0]
        tileval = 4 if random.random() > 0.8 else 2  # assuming a 4:1 distribution ratio
        row, col = random.choice(empty_pos)
        self.board[row, col] = tileval

    def getLegalMoves(self):
        self.legalMoves = set()
        if self.countZeros() > 0:
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row, col] == 0:
                        def checkNeighbors(self, row, col):
                            if row - 1 in range(self.size) and self.board[row - 1, col] > 0:
                                self.legalMoves.add(2)
                            if row + 1 in range(self.size) and self.board[row + 1, col] > 0:
                                self.legalMoves.add(0)
                            if col - 1 in range(self.size) and self.board[row, col - 1] > 0:
                                self.legalMoves.add(1)
                            if col + 1 in range(self.size) and self.board[row, col + 1] > 0:
                                self.legalMoves.add(3)
                        checkNeighbors(self, row, col)

        # Check for horizontal matches
        for row in range(self.size):
            for col in range(self.size - 1):
                if self.board[row, col] == self.board[row, col + 1] != 0:
                    self.legalMoves.update([1, 3])
                    break

        # Check for vertical matches
        for row in range(self.size - 1):
            for col in range(self.size):
                if self.board[row, col] == self.board[row + 1, col] != 0:
                    self.legalMoves.update([0, 2])
                    break

        return self.legalMoves

    def isEnd(self):
        return len(self.getLegalMoves()) == 0

    def countZeros(self):
        return np.count_nonzero(self.board == 0)
        
    def getHighest(self):
        max = self.board[0,0]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i,j] > max:
                    max = self.board[i,j]
        return max

    '''
    ----------------------
    GAME RUNNING FUNCTIONS
    ----------------------
    ''' 

    def swipeLeft(self):
        for m in range(self.size):
            row = self.board[m, :]
            if sum(row) == 0: continue
            row = row[row != 0]
            rowlist = row.tolist()
            for i in xrange(row.size - 1):
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
            for i in xrange(row.size - 1, 0, -1):
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
            for i in xrange(row.size - 1):
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
            for i in xrange(row.size - 1, 0, -1):
                if rowlist[i] == rowlist[i - 1]:
                    rowlist[i] *= 2
                    self.score += rowlist[i]
                    rowlist[i - 1] = 0
            newrow = np.array(filter(lambda x: x != 0, rowlist))
            self.board[:, m] = np.concatenate((np.zeros(self.size - newrow.size), newrow))

    """
    '''
    ---------------------
    INTERACTION FUNCTIONS
    ---------------------
    '''
    
    # should return a list of new boards
    def generateSuccessor(self, action):
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
        post_actions = [copy.copy(pre_action) for i in range(len(empty_pos))]
        for i in range(len(post_actions)):
            row, col = empty_pos[i]
            post_actions[i].placeTile(row, col)
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
    """
