import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1a_problem:
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState: GameState = gameState
        self.costFn = 0
        self.goal = (0, 0)

    @log_function
    def getStartState(self):
        return self.startingGameState

    @log_function
    def isGoalState(self, state):
        return self.startingGameState.hasFood(state[0], state[1])

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        # ------------------------------------------
        "*** YOUR CODE HERE ***"
        successors = []

        if not self.startingGameState.hasWall(state[0] - 1, state[1]):
            successors.append(((state[0] - 1, state[1]), 'West', 1))
        
        if not self.startingGameState.hasWall(state[0] + 1, state[1]):
            successors.append(((state[0] + 1, state[1]), 'East', 1))
        
        if not self.startingGameState.hasWall(state[0], state[1] + 1):
            successors.append(((state[0], state[1] + 1), 'North', 1))
        
        if not self.startingGameState.hasWall(state[0], state[1] - 1):
            successors.append(((state[0], state[1] - 1), 'South', 1))
        
        return successors