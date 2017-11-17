import collections, random
import gamestate
import player

def play2048():
    game = gamestate.Game_2048()
    def evalFn(currentGameState):
        weights = [range(i,i+4) for i in range(1,5)]
        sum = 0.0
        for i in range(4):
            for j in range(4):
                sum += weights[i][j] * currentGameState.board[i,j]
        return currentGameState.getScore() + sum
    agent = player.Player(2, evalFn)
    while not game.isEnd():
        action = agent.getAction(game.copy())
        print "Action: " + str(action)
        game.swipe(action)
        game.placeRandomTile()
        game.printScore()
        game.printBoard()


play2048()
