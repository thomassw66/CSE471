# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from collections import defaultdict

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node:
    """
        Nodes contain state as well info about parent and action taken from that parent
        When a solution is found we can call path to generate the list of actions it took 
        to reach this node.
    """
    def __init__(self, state, parent=None, action=None, pathcost=0, depth=0):
        # initialize
        self.state = state
        self.parent = parent
        self.action = action 
        self.pathcost = pathcost 
        if parent: 
            self.depth = parent.depth + 1
        else:
            self.depth = depth 

    def __repr__(self):
        return "%s" % self.state

    def path(self):
        """
        Nodes form a linked list data structure. 
            To generate the actions to a node we traverse the list, adding actions to the path
            until we reach the root node (whose parent will be None)
        """
        x, actions = self, []
        while x.parent:
            actions.insert(0, x.action)
            x = x.parent
        return actions

def genericGraphSearch(problem, frontier):
    visited = {}
    frontier.push(Node(problem.getStartState()))
    while frontier:
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return node.path()
        """ 
        IMPORTANT DISTINCTION
         We ONLY expand nodes that have not been visited,
         but we add all the nodes reachable from node to the frontier (regardless of whether or not theyve been visited)
            I spent a lot of time scratching my head about this... 
            there may be visited nodes in the frontier
         """
        if node.state not in visited:
            visited[node.state] = True
            for state, act, step in problem.getSuccessors(node.state):
                n = Node(state, node, act, node.pathcost + step)
                frontier.push(n)
    return None


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    
    "*** YOUR CODE HERE ***"
    return genericGraphSearch(problem, util.Stack())


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return genericGraphSearch(problem, util.Queue())

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
        Uniform Cost Search is the same as A* search with f(n) = g(n)
    """
    return aStarSearch(problem, nullHeuristic)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return genericGraphSearch(problem, util.PriorityQueueWithFunction(pathmax_correction(lambda n: heuristic(n.state, problem) + n.pathcost)))

# Takes an inconsistent heuristic 
def pathmax_correction(f):
    memo = {}
    def helper(n):
        if n.parent in memo:
            memo[n] = max(memo[n.parent], f(n))
        else:
            memo[n] = f(n)
        return memo[n]
    return helper

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
