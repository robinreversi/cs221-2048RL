import collections, random, operator
import gamestate
import player

def play2048():
    games = [gamestate.Game_2048() for _ in range(4)]
    # game = gamestate.Multi_Game_2048(4)
    def evalFn(currentGameState):
        '''
        if currentGameState.isEnd():
            return float('-inf')
        weights = [range(i,i+4) for i in range(1,5)]
        sum = 0.0
        for i in range(4):
            for j in range(4):
                sum += weights[i][j] * currentGameState.board[i,j]
        '''
        return currentGameState.getScore() #+ sum
    agent = player.Player(2, evalFn)
    done = False
    while not done:
        values = collections.defaultdict(float)
        count = collections.defaultdict(float)
        for game in games:
            action,vals = agent.getAction(game.copy())
            print "Action: " + str(action)
            for move,score in vals:
                values[move] += score
                count[move] += 1

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
        print('Current score is ', total)



####################################################

def main():
    play2048()


if __name__ == '__main__':
    main()
