import collections, random, operator
import bitstate
import matplotlib.pyplot as plt
import numpy as np
import player
import matplotlib.pyplot as plot
import time

def play2048(num_boards):
    games = [bitstate.Game_2048.fromNew() for _ in range(num_boards)]
    # game = gamestate.Multi_Game_2048(4)
    def evalFn(currentGameState):
        if currentGameState.isEnd():
            return float('-inf')
        weights = [range(i, i + 4) for i in range(1, 5)]
        sum = 0.0
        for i in range(4):
            for j in range(4):
                sum += weights[i][j] * currentGameState.bitToBoard()[i,j]
        return currentGameState.getScore() + sum

    agent = player.Player(2, evalFn)
    done = False
    total = 0.0
    moves = 0
    while not done:
        values = collections.defaultdict(float)
        count = collections.defaultdict(float)
        for game in games:
            start = time.time()
            action,vals = agent.getAction(bitstate.Game_2048.fromOld(game.board,game.tableL,game.tableR))
            end = time.time()
            print ('Get action time: ', end - start)
            print "Action: " + str(action)
            for move,score in vals:
                values[move] += score
                count[move] += 1
            print vals
        for key in values:
            values[move] /= count[move]
        action = max(values.iteritems(), key=operator.itemgetter(1))[0]
        total = 0.0
        for game in games:
            game.swipe(action)
            game.placeRandomTile()
            total += game.getScore()
            game.printBoard()
            if game.isEnd():
                done = True
        moves += 1
        if moves == 10:
            print ''
    return total / num_boards



####################################################

def main():
    play2048(1)
    '''
    averages = []
    for board_size in range(2,9):
        lst = []
        for _ in range(5):
            print _
            lst.append(play2048(board_size))
        averages.append(sum(lst) / 10)
    plot.scatter(range(2,9),averages)
    plot.xlabel('Board Size')
    plot.ylabel('Average Score per Board')
    plot.show()
    '''


if __name__ == '__main__':
    main()
