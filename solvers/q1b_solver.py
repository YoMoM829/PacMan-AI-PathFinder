#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

def q1b_solver(problem: q1b_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

from collections import defaultdict
import math

class AStarData:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.priority_queue = util.PriorityQueue()
        self.goals = []
        self.actions = []
        self.distance = defaultdict(lambda: float('inf'))  # Default to infinity for new states
        self.predecessor = {}
        self.explored = set()

def astar_initialise(problem: q1b_problem):
    start = problem.getStartState()
    coords = start.getPacmanPosition()
    astarData = AStarData(coords[0], coords[1])
    astar_find_goal(problem, astarData)
    astarData.distance[coords] = 0
    astarData.priority_queue.push(coords, 0)
    return astarData

def astar_loop_body(problem: q1b_problem, astarData: AStarData):
    current_state = astarData.priority_queue.pop()

    if problem.isGoalState(current_state):
        return astar_goal(problem, astarData, current_state)

    if current_state in astarData.explored:
        return (False, astarData.actions)

    astarData.explored.add(current_state)
    successors = problem.getSuccessors(current_state)

    for successor in successors:     
        successor_position = successor[0]
        new_cost = astarData.distance[current_state] + successor[2]

        if new_cost < astarData.distance[successor_position]:
            astarData.distance[successor_position] = new_cost
            heuristic_distance = new_cost + astar_heuristic(successor_position, astarData.goals, 1.5)
            astarData.priority_queue.update(successor[0], heuristic_distance)
            astarData.predecessor[successor_position] = (successor[1], current_state)

    return (False, astarData.actions)

def astar_heuristic(current, goals, weight):
    min = math.inf
    for goal in goals:
        val = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        if val < min:
            min = val
    return min * weight

def astar_goal(problem: q1b_problem, astarData: AStarData, state_pos):
    start = problem.getStartState().getPacmanPosition()
    while state_pos != start:
        action, state_pos = astarData.predecessor[state_pos]
        astarData.actions.append(action)
    astarData.actions.reverse()
    return (True, astarData.actions)

def astar_find_goal(problem: q1b_problem, astarData: AStarData):
    grid = problem.getStartState().getFood()
    for x, row in enumerate(grid):
        for y, column in enumerate(row):
            if column:
                astarData.goals.append((x, y))