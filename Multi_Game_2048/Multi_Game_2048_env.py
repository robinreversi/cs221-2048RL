import gym
from gym import spaces
from gym.utils import seeding
import copy

from Multi_Game_2048 import gameutil

util = gameutil.gameutil()

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
    metadata = {'render.modes': ['human', 'ansi']}
    def __init__(self):

        self.n = 4
        self.boards = [util.newBoard() for _ in range(self.n)]
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.MultiDiscrete([range(16) for _ in range(self.n * 16)])
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
        observation = []
        for k in range(self.n):
            prevScore = util.getScore(self.boards[k])
            prevBoard = self.boards[k]
            self.boards[k] = util.swipe(action, self.boards[k])
            if prevBoard != self.boards[k]:
                self.boards[k] = util.placeRandomTile(self.boards[k])
            reward += util.getScore(self.boards[k]) - prevScore
            if util.isEnd(self.boards[k]):
                done = True
            observation += util.bitToBoardPower(self.boards[k]).flatten().tolist()

        self.score += (reward / self.n)

        return np.asarray([observation]), reward, done, dict()
    
    def _reset(self):
        """Reset the board to begin a new game. Places two random tiles on the board."""
        self.boards = [util.newBoard() for _ in range(self.n)]
        self.score = 0
        self.legalMoves = set()
        observation = []
        for k in range(self.n):
            observation += util.bitToBoard(self.boards[k]).flatten().tolist()
        return np.array([observation])
    
    def _render(self, mode='human', close=False):
        if close:
            return
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        s = 'Score: {}\n'.format(self.score)
        for board in self.boards:
            s += "{}\n\n".format(util.bitToBoard(board))
        outfile.write(s)
        return outfile

    ############### Non-OpenAI Gym functions ###############

    def updateScore(self):
        self.score = sum(util.getScore(self.boards[k]) for k in range(self.n)) / float(self.n)

    def updateLegalMoves(self):
        legalMoves = util.getLegalMoves(self.boards[0])
        for k in range(1, self.n):
            legalMoves = set.union(legalMoves, util.getLegalMoves(self.boards[k]))
        self.legalMoves = legalMoves

    def isEnd(self):
        for k in range(self.n):
            if util.isEnd(self.boards[k]): 
                return True
        return False

    def getScore(self):
        self.updateScore()
        return self.score

    def getLegalMoves(self):
        self.updateLegalMoves()
        return self.legalMoves

