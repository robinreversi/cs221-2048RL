import random
import time
import numpy as np
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
                '''
                #start = time.time()
                newStates = [gameState.generateSuccessor(action) for action in legalMoves]
                #mid = time.time()
                scores = []
                state_vals = [[evalFn(item) for item in lst] for lst in newStates]
                for i in range(len(newStates)):
                    lst = state_vals[i]
                    inds = np.argsort(lst)
                    if len(inds) > 4:
                        inds = inds[[0,1,-1,-2]]

                    sample_states = [newStates[i][k] for k in inds]
                    potential_scores = [1.0 / len(sample_states) * V(newState, depth - 1, evalFn)[0] for newState in sample_states]
                    avg_score = sum(potential_scores)
                    scores.append(avg_score)
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                move_value_pairings = [(move, scores[i]) for i, move in enumerate(legalMoves)]
                #end = time.time()
                return (bestScore, legalMoves[chosenIndex], move_value_pairings)
                '''
                
                newStates = [gameState.generateSuccessor(action) for action in legalMoves]
                scores = []
                for i in range(len(newStates)):
                    potential_score = V(newStates[i], depth - 1, evalFn)[0]
                    scores.append(potential_score)
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                move_value_pairings = [(move, scores[i]) for i, move in enumerate(legalMoves)]
                return (bestScore, legalMoves[chosenIndex], move_value_pairings)
                
                
        value, chosenMove, move_value_pairings = V(gameState, self.depth, self.evalFn)
        return (chosenMove, move_value_pairings)
