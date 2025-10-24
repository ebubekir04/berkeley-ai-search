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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # skeletcode kregen we deels in de WPO

    # problem.getStartState() print A
    # problem.isGoalState(problem.getStartState()) print False
    # problem.getSuccessors(problem.getStartState()) print
    # [('B', '0:A->B', 1.0), ('C', '1:A->C', 2.0), ('D', '2:A->D', 4.0)]

    fringe = util.Stack()  # agenda
    start = problem.getStartState()  # startState (moet niet, maar is praktischer)
    closed = set()  # hierin worden de bezochte nodes opgeslagen, initieel leeg
    fringe.push((start, []))  # push startState en een lege lijst (visited nodes) in de stack, eerste stap DFS

    while not fringe.isEmpty():  # Als de stack leeg is, is er geen oplossing
        node = fringe.pop()  # pop de laatste node uit de stack
        current = node[0]  # current neemt de state van de node
        path = node[1]  # path neemt de lijst van visited nodes

        if problem.isGoalState(current):  # check of de huidige node de goal is
            return path
        else:
            if current not in closed:  # Vermijden dat een node meerdere keren wordt bezocht
                closed.add(current)
                volgendeStatesDFS = problem.getSuccessors(current)  # op vraag van de opgave, de volgende nodes
                for child, action, stepCost in volgendeStatesDFS:  # for-loop om de volgende nodes op te slaan in agenda
                    fringe.push((child, path + [action]))  # we bouwen een pad op met de acties tot de goal


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    fringe = util.Queue()  # agenda, deze keer een queue
    start = problem.getStartState()
    closed = set()
    fringe.push((start, []))

    while not fringe.isEmpty():
        node = fringe.pop()
        current = node[0]
        path = node[1]

        if problem.isGoalState(current):
            return path
        else:
            if current not in closed:
                closed.add(current)
                volgendeStatesBFS = problem.getSuccessors(current)  # op vraag van de opgave, de volgende nodes
                for child, action, stepCost in volgendeStatesBFS:
                    fringe.push((child, path + [action]))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # enige verschil met DFS en BFS is dat de priorityqueue gebruikt wordt en dat de stepCost wordt meegegeven

    fringe = util.PriorityQueue()  # PriorityQueue
    start = problem.getStartState()
    closed = set()
    fringe.push((start, [], 0), 0)  # stepCost initieel 0, priority initieel 0

    while not fringe.isEmpty():
        node = fringe.pop()
        current = node[0]
        path = node[1]

        if problem.isGoalState(current):
            return path
        else:
            if current not in closed:
                closed.add(current)
                volgendeStatesUCS = problem.getSuccessors(current)  # op vraag van de opgave, de volgende nodes
                for child, action, stepCost in volgendeStatesUCS:
                    stepCost = problem.getCostOfActions(path + [action])  # bereken de totale kost van de acties
                    fringe.push((child, path + [action]), stepCost)  # push verwacht een tuple, item en priority


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # verschil met UCS is dat de priorityqueue de totale kost + de heuristic krijgt

    fringe = util.PriorityQueue()
    start = problem.getStartState()
    closed = set()
    fringe.push((start, [], 0), 0 + heuristic(start, problem))  # heuristic is de geschatte afstand tot de goal

    while not fringe.isEmpty():
        node = fringe.pop()
        current = node[0]
        path = node[1]

        if problem.isGoalState(current):
            return path
        else:
            if current not in closed:
                closed.add(current)
                volgendeStatesAstar = problem.getSuccessors(current)  # op vraag van de opgave, de volgende nodes
                for child, action, stepCost in volgendeStatesAstar:
                    stepCost = problem.getCostOfActions(path + [action])
                    # heuristic berekent de afstand tot de goal, deze wordt toegevoegd aan de totale kost
                    fringe.push((child, path + [action]), stepCost + heuristic(child, problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
