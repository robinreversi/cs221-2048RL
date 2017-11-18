import collections, random
import gamestate
import matplotlib.pyplot as plt
import numpy as np
import player

def play2048():
    game = gamestate.Game_2048()
    def evalFn(currentGameState):
        weights = [[7,6,5,4],[6,5,4,3],[5,4,3,2],[4,3,2,1],[3,2,1,0]]
        sum = 0.0
        for i in range(4):
            for j in range(4):
                sum += weights[i][j] * currentGameState.board[i,j]
        return currentGameState.getScore() + sum

    scores = []
    for _ in range(1):
        game = gamestate.Game_2048()
        print _
        agent = player.Player(2, evalFn)
        while not game.isEnd():
            action = agent.getAction(game.copy())[0]
            print "Action: " + str(action)
            game.swipe(action)
            game.placeRandomTile()
            game.printScore()
            game.printBoard()
        scores.append(game.getScore())
    
    scores = np.array(scores)
    average = scores.sum() / 50
    variance = np.sum((scores - average) ** 2)  / 50
    plt.scatter(range(50), scores)
    plt.xlabel('trial')
    plt.ylabel('score')
    plt.plot(range(50), [average for _ in range(50)], 'b')
    plt.show()
    print average
    print variance
play2048()
