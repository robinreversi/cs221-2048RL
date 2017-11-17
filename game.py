import collections, random
import gamestate
import player

def play2048():
    game = gamestate.Game_2048()
    def evalFn(currentGameState):
        return currentGameState.getScore()
    agent = player.Player(2, evalFn)

    while not game.isEnd():
        action = agent.getAction(game.copy())
        game.getMove(action)
        game.placeRandomTile()
        game.printScore()
        game.printBoard()


play2048()
