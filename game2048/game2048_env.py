import gym
from gym import spaces
from gym.utils import seeding

import numpy as np
import random

import itertools
import logging
from six import StringIO
import sys


class Game2048Env(gym.Env):
    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self):
        self.size = 4
        self.board = np.zeros((self.size, self.size))
        self.score = 0
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0, 2**(self.size ** 2), (self.size ** 2))
        self.legalMoves = set()
        self.placeRandomTile()
        self._seed()
        self._reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        """Perform one step of the game. This involves moving and adding a new tile."""
        prev_score = self.score
        if(action == 0):
            self.swipeUp()
        elif(action == 1):
            self.swipeRight()
        elif(action == 2):
            self.swipeDown()
        else:
            self.swipeLeft()
        reward = self.score - prev_score
        done = self.isEnd()
        #print("Am I done? {}".format(done))        
        observation = self.board.flatten()
        info = dict()
        return observation, reward, done, info
        # Return observation (board state), reward, done and info dict

    def _reset(self):
        """Reset the board to begin a new game. Places two random tiles on the board."""
        self.board = np.zeros((self.size, self.size))
        self.score = 0
        self.legalMoves = set()
        
        logging.debug("Adding tiles")
        
        self.placeRandomTile()
        self.placeRandomTile()

        return self.Matrix.flatten()

    def _render(self, mode='human', close=False):
        if close:
            return
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        s = 'Score: {}\n'.format(self.score)
        s += "{}\n".format(self.board)
        outfile.write(s)
        return outfile
        
    ###########################################################
    
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
                                self.legalMoves.update(2)
                            if row + 1 in range(self.size) and self.board[row + 1, col] > 0:
                                self.legalMoves.update(0)
                            if col - 1 in range(self.size) and self.board[row, col - 1] > 0:
                                self.legalMoves.update(1)
                            if col + 1 in range(self.size) and self.board[row, col + 1] > 0:
                                self.legalMoves.update(3)
                        checkNeighbors(self, row, col)

        # Check for horizontal matches
        for row in range(self.size):
            for col in range(self.size - 1):
                if self.board[row, col] == self.board[row, col + 1] != 0:
                    self.legalMoves.update(1, 3)
                    break

        # Check for vertical matches
        for row in range(self.size - 1):
            for col in range(self.size):
                if self.board[row, col] == self.board[row + 1, col] != 0:
                    self.legalMoves.update(0, 2)
                    break

        return self.legalMoves

    def isEnd(self):
        return len(self.getLegalMoves()) == 0

    def countZeros(self):
        return np.count_nonzero(self.board == 0)

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
    