#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def q1c_solver(problem: q1c_problem):
    result = []
    num_expansions = 0
    while problem.goals:
        astarData = astar_initialise(problem)
        terminate = False
        while not terminate:
            num_expansions += 1
            terminate, partial_result = astar_loop_body(problem, astarData)
            if terminate == True:
                result.extend(partial_result)  # Append the path for this goal
    print(f'Number of node expansions: {num_expansions}')
    return result

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

def astar_initialise(problem: q1c_problem):
    start = problem.pos 
    astarData = AStarData(start[0], start[1])
    astarData.distance[start] = 0
    astarData.priority_queue.push(start, 0)
    return astarData

def astar_loop_body(problem: q1c_problem, astarData: AStarData):
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
            heuristic_distance = new_cost + astar_heuristic(successor_position, astarData.goals)
            astarData.priority_queue.update(successor[0], heuristic_distance)
            astarData.predecessor[successor_position] = (successor[1], current_state)

    return (False, astarData.actions)

def astar_heuristic(current, goals):
    min = math.inf
    for goal in goals:
        val = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        if val < min:
            min = val
    return min

def astar_goal(problem: q1c_problem, astarData: AStarData, state_pos):
    initial = state_pos
    start = problem.pos
    while state_pos != start:
        action, state_pos = astarData.predecessor[state_pos]
        astarData.actions.append(action)
    # Remove the collected goal from the list
    problem.goals.remove(initial)
    problem.pos = initial
    astarData.actions.reverse()
    
    return (True, astarData.actions)