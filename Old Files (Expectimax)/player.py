import random
import time
class Player:

    def __init__(self, depth, evalFn):
        self.evalFn = evalFn
        self.depth = depth


    def getAction(self, gameState):
        def V(gameState, depth, evalFn):
            legalMoves = gameState.options
            if(gameState.isEnd()):
                return (gameState.getScore(), 'w')
            elif(depth == 0):
                return (evalFn(gameState), random.choice(legalMoves))
            else:
                start = time.time()
                newStates = [gameState.generateSuccessor(action) for action in legalMoves]
                mid = time.time()
                scores = []
                for i in range(len(newStates)):
                    num_states = len(newStates[i])
                    potential_scores = [1.0 / num_states * V(newState, depth - 1, evalFn)[0] for newState in newStates[i]]
                    avg_score = sum(potential_scores)
                    scores.append(avg_score)
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                move_value_pairings = [(move, scores[i]) for i, move in enumerate(legalMoves)]
                end = time.time()
                return (bestScore, legalMoves[chosenIndex], move_value_pairings)
            
        value, chosenMove, move_value_pairings = V(gameState, self.depth, self.evalFn)
        return (chosenMove, move_value_pairings)
