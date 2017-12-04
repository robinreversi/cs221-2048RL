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
    weights1 = [range(i,i+4) for i in xrange(1,5)]
    weights2 = [range(i+3, i-1,-1) for i in xrange(1, 5)]
    weights3 = [range(i+3, i-1,-1) for i in xrange(4, 0,-1)]
    weights4 = [range(i, i + 4) for i in xrange(4, 0,-1)]
    print weights1
    print weights2
    print weights3
    print weights4

    def evalFn(currentGameState):
        if currentGameState.isEnd():
            return float('-inf')

        def weightedGrid(currentGameState):
            sum1 = 0.0
            sum2 = 0.0
            sum3 = 0.0
            sum4 = 0.0
            for i in xrange(4):
                for j in xrange(4):
                    sum1 += weights1[i][j] * currentGameState.board[i, j]
                    sum2 += weights2[i][j] * currentGameState.board[i, j]
                    sum3 += weights3[i][j] * currentGameState.board[i, j]
                    sum4 += weights4[i][j] * currentGameState.board[i, j]
            return max(sum1, sum2, sum3, sum4)

        def monotonicity(cGS, k=10.0):

            def monoEval(a, b, e=1.0):
                # if a == b: b += 1  # make [ v ][ v ] the same as [ v ][ v+1 ]
                if a == b: return 2 * k
                return k / (np.log2(b / a) ** e)
            sum = 0.0

            for r in xrange(4):
                forw = 0.0
                back = 0.0
                for k in xrange(3):
                    forw += monoEval(cGS.board[r, k], cGS.board[r, k+1])
                    back += monoEval(cGS.board[r, k+1], cGS.board[r, k])
                sum += max(forw, back)

            for c in xrange(4):
                forw = 0.0
                back = 0.0
                for k in xrange(3):
                    forw += monoEval(cGS.board[k, c], cGS.board[k+1, c])
                    back += monoEval(cGS.board[k+1, c], cGS.board[k, c])
                sum += max(forw, back)

            return sum

        def openTilePenalty(cGS, n=5):
            return cGS.countZeros() - n
            # return -((cGS.countZeros() - n) ** 2)

        eval = 0.0
        eval += currentGameState.getScore()
        eval += weightedGrid(currentGameState)
        # eval += monotonicity(currentGameState, k=10.0)
        eval += 50 * openTilePenalty(currentGameState)

        return eval

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
    for i in range(8):
        curr_score,highest = play2048(2)
        score += curr_score
        lst.append(highest)
        dict[max(highest)] += 1
    print ("Average: ", score / 8.0)
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
