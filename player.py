import random

class Player:

    def __init__(self, depth, evalFn):
        self.evalFn = evalFn
        self.index = 0


    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
        def V(agentIndex, numAgents, gameState, depth, evalFn):
            agentIndex = agentIndex % numAgents
            legalMoves = gameState.getLegalActions(agentIndex)
            if(gameState.isEnd()):
                return (gameState.getScore(), 'w')
            elif(depth == 0):
                return (evalFn(gameState), random.choice(legalMoves))
            elif(agentIndex == 0):
                newStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
                scores = [V(agentIndex + 1, numAgents, newState, depth, evalFn)[0] for newState in newStates]
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return (bestScore, legalMoves[chosenIndex])
            elif(agentIndex > 0 and agentIndex < numAgents - 1):
                newStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
                scores = [1.0 / len(legalMoves) * V(agentIndex + 1, numAgents, newState, depth, evalFn)[0] for newState in newStates]
                expectedScore = sum(scores)
                return (expectedScore, legalMoves[0])
            else:
                newStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
                scores = [1.0 / len(legalMoves) * V(agentIndex + 1, numAgents, newState, depth - 1, evalFn)[0] for newState in newStates]
                expectedScore = sum(scores)
                return (expectedScore, legalMoves[0])

        agentIndex = self.index
        numAgents = gameState.getNumAgents()
        value, chosenMove = V(agentIndex, numAgents, gameState, self.depth, self.evalFn)
        return chosenMove
