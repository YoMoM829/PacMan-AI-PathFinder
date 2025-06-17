import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1c_problem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.
    Some useful data has been included here for you
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goals: A position in the gameState
        """
        self.startingGameState: GameState = gameState
        self.costFn = 0
        self.goals = []
        self.pos = gameState.getPacmanPosition()
        grid = self.startingGameState.getFood()
        for x, row in enumerate(grid):
            for y, column in enumerate(row):
                if column:
                    self.goals.append((x, y))

    @log_function
    def getStartState(self):
        return self.startingGameState

    @log_function
    def isGoalState(self, state):
        if state in self.goals:
            return True
        return False

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