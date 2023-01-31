# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        total_score = successorGameState.getScore()


        foodList = []
        for food in newFood.asList():
            foodList.append(manhattanDistance(newPos, food))
        if len(foodList) > 0:
            nearestFoodDist = min(foodList)
            if nearestFoodDist != 0:
                total_score += 0.92 / nearestFoodDist

        ghostList = []
        for ghost in newGhostStates:
            ghostList.append(manhattanDistance(newPos, ghost.getPosition()))
        if len(ghostList) > 0:
            nearestGhostDist = min(ghostList)
            if nearestGhostDist != 0:
                total_score -= 1 / nearestGhostDist

        return total_score

        

            

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def value(state, ind, level):
            if state.isWin() or state.isLose() or state.getNumAgents() * self.depth <= level: 
                return self.evaluationFunction(state)
            if ind == 0:
                return max_value(state, ind, level)
            return min_value(state, ind, level)
              
        def max_value(state, ind, level):
            v = -1 * float('inf')
            for move in state.getLegalActions(0):
                v = max(v, value(state.generateSuccessor(ind, move), (level+1) % state.getNumAgents(), (level+1)))
            return v
            
        def min_value(state, ind, level):
            v = float("inf")
            for move in state.getLegalActions(ind):
                v = min(v, value(state.generateSuccessor(ind, move), (level+1) % state.getNumAgents(), (level+1)))
            return v
        
        total_array = []
        for move in gameState.getLegalActions(0):
            total_array.append(value(gameState.generateSuccessor(0, move), 1, 1))
        return gameState.getLegalActions(0)[total_array.index(max(total_array))]
        
    

    
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def value(state, ind, level, a, b):
            if state.isWin() or state.isLose() or state.getNumAgents() * self.depth <= level: 
                return self.evaluationFunction(state)
            if ind == 0:
                return max_value(state, ind, level, a, b)
            return min_value(state, ind, level, a, b)
              
        def max_value(state, ind, level, a, b):
            v = -1 * float('inf')
            for move in state.getLegalActions(0):
                v = max(v, value(state.generateSuccessor(ind, move), (level+1) % state.getNumAgents(), (level+1), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v
            
        def min_value(state, ind, level, a, b):
            v = float("inf")
            for move in state.getLegalActions(ind):
                v = min(v, value(state.generateSuccessor(ind, move), (level+1) % state.getNumAgents(), (level+1), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        a = -1 * float('inf')
        b = float('inf')
        result = (-1 * float('inf'), '')
        for move in gameState.getLegalActions(0):
            val = value(gameState.generateSuccessor(0, move), 1 % gameState.getNumAgents(), 1, a, b)
            if val > result[0]:
                result = (val, move)
                if val > b:
                    return result[1]
                a = max(a, val)
        return result[1]
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def value(state, ind, level):
            if state.isWin() or state.isLose() or state.getNumAgents() * self.depth <= level: 
                return self.evaluationFunction(state)
            if ind == 0:
                return max_value(state, ind, level)
            return expectation(state, ind, level)
              
        def max_value(state, ind, level):
            v = -1 * float('inf')
            for move in state.getLegalActions(0):
                v = max(v, value(state.generateSuccessor(ind, move), (level+1) % state.getNumAgents(), (level+1)))
            return v

        def expectation(state, ind, level):
            total_array = [value(state.generateSuccessor(ind, move), (level+1) % state.getNumAgents(), (level+1)) for move in state.getLegalActions(ind)]
            return sum(total_array) / len(total_array)

        total_array = []
        for move in gameState.getLegalActions(0):
            total_array.append(value(gameState.generateSuccessor(0, move), 1, 1))
        return gameState.getLegalActions(0)[total_array.index(max(total_array))]

        



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I calculated the nearest food and ghost distances.
    Then, I divided 0.92 which is the weight that I gave to the nearest food distance
    and added it to the total score. On the other hand, I divided 1 to the nearest ghost distance
    and subtracted it from the total score. I also added the current score to the total score.
    Lastly, I subtracted the number of capsules times 32 which is a weight that I gave to the capsules
    from total score.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    
    total_score = currentGameState.getScore()

    
    foodList = []
    for food in newFood.asList():
        foodList.append(manhattanDistance(newPos, food))
    if len(foodList) > 0:
        nearestFoodDist = min(foodList)
        if nearestFoodDist != 0:
            total_score += 0.92 / nearestFoodDist

    ghostList = []
    for ghost in newGhostStates:
        ghostList.append(manhattanDistance(newPos, ghost.getPosition()))
    if len(ghostList) > 0:
        nearestGhostDist = min(ghostList)
        if nearestGhostDist != 0:
            total_score -= 1 / nearestGhostDist

    total_score -= 32*len(currentGameState.getCapsules())

    return total_score


# Abbreviation
better = betterEvaluationFunction
