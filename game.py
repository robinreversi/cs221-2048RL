import collections, random
import gamestate
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
    agent = player.Player(2, evalFn)
    while not game.isEnd():
        action = agent.getAction(game.copy())
        print "Action: " + str(action)
        game.swipe(action)
        game.placeRandomTile()
        game.printScore()
        game.printBoard()


play2048()
