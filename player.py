import random

class Player:

    def __init__(self, depth, evalFn):
        self.evalFn = evalFn
        self.depth = depth


    def getAction(self, gameState):
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
                    num_states = len(newStates[i])
                    potential_scores = [1.0 / num_states * V(newState, depth - 1, evalFn)[0] for newState in newStates[i]]
                    avg_score = sum(potential_scores)
                    scores.append(avg_score)

                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return (bestScore, legalMoves[chosenIndex])
            
        value, chosenMove = V(gameState, self.depth, self.evalFn)
        return chosenMove
