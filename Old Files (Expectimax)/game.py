import collections, random, operator
import bitstate
import gamestate
import matplotlib.pyplot as plt
import numpy as np
import player
import matplotlib.pyplot as plot
import time

def play2048(num_boards):
    games = [gamestate.Game_2048() for _ in range(num_boards)]
    # game = gamestate.Multi_Game_2048(4)
    weights1 = [range(i,i+4) for i in range(1,5)]
    weights2 = [xrange(i+3, i-1,-1) for i in range(1, 5)]
    weights3 = [xrange(i+3, i-1,-1) for i in xrange(4, 0,-1)]
    weights4 = [range(i, i + 4) for i in xrange(4, 0,-1)]
    print weights1
    print weights2
    print weights3
    print weights4
    def evalFn(currentGameState):
        if currentGameState.isEnd():
            return float('-inf')
        sum1 = 0.0
        sum2 = 0.0
        sum3 = 0.0
        sum4 = 0.0
        for i in range(4):
            for j in range(4):
                sum1 += weights1[i][j] * currentGameState.board[i,j]
                sum2 += weights2[i][j] * currentGameState.board[i, j]
                sum3 += weights3[i][j] * currentGameState.board[i, j]
                sum4 += weights4[i][j] * currentGameState.board[i, j]

        return currentGameState.getScore() + sum1

    agent = player.Player(2, evalFn)
    done = False
    total = 0.0
    moves = 0
    highest_tile = []
    while not done:
        values = collections.defaultdict(float)
        count = collections.defaultdict(float)
        for game in games:
            start = time.time()
            action,vals = agent.getAction(game.copy())
            end = time.time()
            print("Time: ", end - start)
            print "Action: " + str(action)
            for move,score in vals:
                values[move] += score
                count[move] += 1
        for key in values:
            values[move] /= count[move]
        action = max(values.iteritems(), key=operator.itemgetter(1))[0]
        for game in games:
            game.swipe(action)
            game.placeRandomTile()
            game.printBoard()
            print ("Score: ",game.getScore())
            if game.isEnd():
                total += game.getScore()
                highest_tile.append(game.getHighest())
                games.remove(game)
        if float(len(games)) < float(1 * num_boards):
            for game in games:
                total += game.getScore()
                highest_tile.append(game.getHighest())
            done = True
    return total / float(num_boards),highest_tile



####################################################

def main():
    score = 0
    lst = []
    dict = collections.defaultdict(int)
    for i in range(2):
        curr_score,highest = play2048(2)
        score += curr_score
        lst.append(highest)
        dict[max(highest)] += 1
    print ("Average: ", score/ 10.0)
    for i in lst:
        print("Highest tile for all board: ",i)
        print("Highest tile for 1 board: ",max(i))
    print dict
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
