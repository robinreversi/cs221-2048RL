import random

class Player:

    def __init__(self, depth, evalFn):
        self.evalFn = evalFn
        self.depth = depth


    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
        def V(gameState, depth, evalFn):
            legalMoves = list(gameState.getLegalMoves())
            if(gameState.isEnd()):
                return (gameState.getScore(), 'w')
            elif(depth == 0):
                return (evalFn(gameState), random.choice(legalMoves))
            else:
                newStates = [gameState.generateSuccessor(action) for action in legalMoves]
                scores = []
                for i in range(len(newStates)):
                    scores.append([V(newState, depth - 1, evalFn)[0] for newState in newStates[i]])
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return (bestScore, legalMoves[chosenIndex])
            
        value, chosenMove = V(gameState, self.depth, self.evalFn)
        return chosenMove
