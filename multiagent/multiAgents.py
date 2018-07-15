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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        x, y = newPos
        m = 1000000
        t = 0
        for fx, fy in newFood.asList():
          d = abs(x - fx) + abs(y - fy) + 1
          t += 1.0 / d 
          m = min(d, m)
        
        g = 0
        for gstate in newGhostStates:
          gx, gy = gstate.getPosition()
          d = abs(x - gx) + abs(y - gy)
          if d == 0:
            g = 800 # Always ensure our agent goes away from ghost right next to it
          else:
            # g = max(g, 1.0 / d)
            g = 0

        return successorGameState.getScore() + t 

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
        """
        "*** YOUR CODE HERE ***"
        # argmax a in actions(s) minvalue(result(s, a))


        legalActions = gameState.getLegalActions(0);
        successors = [gameState.generateSuccessor(0, action) for action in legalActions]
        values = [self.multiAgentSearch(s, 1, 1) for s in successors]
        val, action = max(zip(values, legalActions), key=lambda item: item[0])
        return action 

    def cutoffTest(self, state, depth):
      return depth >= self.depth or self.isTerminal(state)

    def isTerminal(self, state):
      return state.isWin() or state.isLose()

    def multiAgentSearch(self, state, agentIndex, depth):
      if self.isTerminal(state):
        return state.getScore()
      print "minimax"
      n = state.getNumAgents()

      nextAgent = (agentIndex + 1) % n
      nextDepth = depth + 1 if agentIndex == 0 else depth

      if nextDepth <= self.depth:
        actions = state.getLegalActions(agentIndex)
        results = [state.generateSuccessor(agentIndex, s) for s in actions]
        values = [self.multiAgentSearch(r, nextAgent, nextDepth) for r in results ]
        if agentIndex == 0:
          val, action = max(zip(values, actions), key=lambda item: item[0])
          return val
        else: 
          val, action = min(zip(values, actions), key=lambda item: item[0])
          return val
      else:
        actions = state.getLegalActions(agentIndex)
        return max( [self.evaluationFunction(state, a) for a in actions] )

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        print "alpha beta"
        actions = gameState.getLegalActions(0)
        v = -float("inf")
        act = None 
        alpha = -float("inf")
        beta = +float("inf")
        for a in actions:
          s = gameState.generateSuccessor(0, a)
          u = self.value(s, alpha, beta, 1, 1)
          if u > v: 
            act = a
            v = u 
            alpha = max(alpha, v)
        return act

    def worstValue(self, agentIndex):
      if agentIndex == 0: return -float("inf")
      else: return float("inf") 

    def isBetter(self, agentIndex, a, b):
      if agentIndex == 0: return a < b
      else: return a > b 

    def isTerminal(self, state):
      return state.isWin() or state.isLose()

    def value(self, state, alpha, beta, agent_index, depth):
      if self.isTerminal(state): return state.getScore()
      d = depth + 1 if agent_index == 0 else depth 
      if d > self.depth: return state.getScore()
      if agent_index == 0: return self.maxValue(state, alpha, beta, agent_index, depth)
      else: return self.minValue(state, alpha, beta, agent_index, depth)

    # TODO: make this a generic function that takes a (worst value, comparison function)
    def maxValue(self, state, alpha, beta, agent_index, depth):
      v = -float("inf")
      actions = state.getLegalActions(agent_index)
      beta = beta 
      alpha = alpha 
      for a in actions:
        r = state.generateSuccessor(agent_index, a) 

        if depth + 1 > self.depth: 
          v = self.evaluationFunction(state, a)
        else:
          v = max(v, self.value(r, alpha, beta, (agent_index + 1) % state.getNumAgents(), depth + 1 if agent_index == 0 else depth))

        if v > beta: return v 
        alpha = max(alpha, v)
      # print v
      return v  

    def minValue(self, state, alpha, beta, agent_index, depth):
      v = float("inf")
      actions = state.getLegalActions(agent_index)
      beta = beta
      alpha = alpha
      for a in actions:
        r = state.generateSuccessor(agent_index, a)
        v = min(v, self.value(r, alpha, beta, (agent_index + 1) % state.getNumAgents(), depth + 1 if agent_index == 0 else depth))
        if v < alpha: return v 
        beta = min(beta, v)
      # print v 
      return v 


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
        actions = gameState.getLegalActions(0)
        v = -float("inf")
        act = None 
        for a in actions:
          s = gameState.generateSuccessor(0, a)
          u = self.value(s, 1, 1)
          if u > v: 
            act = a
            v = u 
        return act

    def value(self, state, agent_index, depth):
      # print "expecitmax"
      if self.isTerminal(state): return state.getScore()
      d = depth + 1 if agent_index == 0 else depth 
      # if d > self.depth: return state.getScore()
      if agent_index == 0: return self.maxValue(state, agent_index, depth)
      else: return self.expectiValue(state, agent_index, depth)

    def maxValue(self, state, agent_index, depth):
      v = -float("inf")
      actions = state.getLegalActions(agent_index)

      if depth > self.depth and agent_index == 0:
        e = [self.evaluationFunction(state, a) for a in actions]
        print e 
        return e

      for a in actions:
        r = state.generateSuccessor(agent_index, a) 
        v = max(v, self.value(r, (agent_index + 1) % state.getNumAgents(), depth + 1 if agent_index == 0 else depth))
      return v  

    def expectiValue(self, state, agent_index, depth):
      s = 0.0
      actions = state.getLegalActions(agent_index)
      for a in actions:
        r = state.generateSuccessor(agent_index, a)
        v = self.value(r, (agent_index + 1) % state.getNumAgents(), depth + 1 if agent_index == 0 else depth)
        s += v
      return s / float(len(actions))

    def isTerminal(self, state):
      return state.isWin() or state.isLose()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    print "Gello World"
    "*** YOUR CODE HERE ***"
    # the score 
    score = currentGameState.getScore()
    # Legal moves
    legalMoves = gameState.getLegalActions()
    numLegalMoves = len(legalMoves)

    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()

    totalDotDistance = 0
    largestDotDistance = -float("inf")
    closestDotDistance = float("inf")

    x, y = position 
    for fx, fy in food.asList():
      d = abs(x - fx) + abs(y - fy) 
      mind = min(mind, d)
      maxd = max(maxd, d)
    
    g = 0
    for gstate in newGhostStates:
      gx, gy = gstate.getPosition()
      d = abs(x - gx) + abs(y - gy)
      g = min(g, d)
    print ("pussy")
    return  -1.0 

# Abbreviation
better = betterEvaluationFunction

