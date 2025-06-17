import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance 


def scoreEvaluationFunction(currentGameState, Q2_Agent):
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    score = currentGameState.getScore()

    # Penalize distance to the nearest food
    if foodList:
        nearest_food_distance = min(manhattanDistance(pacmanPos, food) for food in foodList)
        score += 10.0 / nearest_food_distance

    # Penalize proximity to active (non-scared) ghosts
    for ghost in ghostStates:
        ghost_distance = manhattanDistance(pacmanPos, ghost.getPosition())
        if ghost.scaredTimer == 0:
            if ghost_distance > 0:
                score -= 10.0 / ghost_distance

    # Reward staying close to capsules if ghosts are near and not scared
    if capsules and any(ghost.scaredTimer == 0 for ghost in ghostStates):
        nearest_capsule_distance = min(manhattanDistance(pacmanPos, cap) for cap in capsules)
        score += 10.0 / nearest_capsule_distance

    # Heavily reward winning, penalize losing
    if currentGameState.isWin():
        score += 10000
    if currentGameState.isLose():
        score -= 10000

    return score

class Q2_Agent(Agent):
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.last_positions = []

    @log_function
    def getAction(self, gameState: GameState):
        logger = logging.getLogger('root')
        logger.info('Agent Decision Making')

        if self.shouldEatGhost(gameState):
            return self.eatGhost(gameState)
        elif self.shouldAvoidGhosts(gameState):
            return self.avoidGhosts(gameState)
        elif self.shouldCollectFood(gameState):
            return self.collectFood(gameState)
        elif self.isPacmanStuck(gameState):
            return self.pacmanUnstuck(gameState)
        else:
            action = self.alpha_beta_search(gameState)
            self.last_positions.append((gameState.getPacmanPosition(), action))
            if len(self.last_positions) > 10:  # Track the last 10 positions
                self.last_positions.pop(0)
            return action
          
    def avoidRevisits(self, position):
        return any(pos == position for pos, _ in self.last_positions)

    def isPacmanStuck(self, gameState: GameState):
        current_position = gameState.getPacmanPosition()
        legal_actions = gameState.getLegalActions(0)
        
        # Check if Pac-Man is repeatedly visiting the same small set of positions
        recent_positions = [pos for pos, _ in self.last_positions[-6:]]
        if recent_positions.count(current_position) > 3:
            return True
        
        # Check if Pac-Man has only one legal action (ignoring STOP)
        non_stop_actions = [action for action in legal_actions if action != Directions.STOP]
        if len(non_stop_actions) <= 1:
            return True

        return False

    def pacmanUnstuck(self, gameState: GameState):
        legal_actions = gameState.getLegalActions(0)
        
        # Try to avoid repeating the last action
        last_action = self.last_positions[-1][1] if self.last_positions else None
        non_stop_actions = [action for action in legal_actions if action != Directions.STOP and action != last_action]
        
        if non_stop_actions:
            return random.choice(non_stop_actions)
        
        # If only one action is available or no better option, try to reverse direction
        opposite_action = Directions.REVERSE[last_action] if last_action else None
        if opposite_action in legal_actions:
            return opposite_action
        
        # As a last resort, take any legal action
        return random.choice(legal_actions)

    def shouldEatGhost(self, gameState: GameState):
        pacman_pos = gameState.getPacmanPosition()
        ghost_states = gameState.getGhostStates()
        return any(manhattanDistance(pacman_pos, ghost.getPosition()) < 3 for ghost in ghost_states if ghost.scaredTimer > 0)

    def shouldAvoidGhosts(self, gameState: GameState):
        pacman_pos = gameState.getPacmanPosition()
        ghost_states = gameState.getGhostStates()
        return any(manhattanDistance(pacman_pos, ghost.getPosition()) < 3 for ghost in ghost_states)

    def shouldCollectFood(self, gameState: GameState):
        food_list = gameState.getFood().asList()
        return len(food_list) > 0 and all(manhattanDistance(gameState.getPacmanPosition(), food) > 1 for food in food_list)

    def eatGhost(self, gameState: GameState):
        ghost_states = gameState.getGhostStates()
        legal_actions = gameState.getLegalActions(0)
        best_action = None
        min_distance = float('inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            successor_pos = successor.getPacmanPosition()
            distance_to_ghosts = min(manhattanDistance(successor_pos, ghost.getPosition()) for ghost in ghost_states)
            
            if distance_to_ghosts < min_distance:
                min_distance = distance_to_ghosts
                best_action = action

        return best_action

    def avoidGhosts(self, gameState: GameState):
        ghost_states = gameState.getGhostStates()
        legal_actions = gameState.getLegalActions(0)
        best_action = None
        max_distance = -float('inf')

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            successor_pos = successor.getPacmanPosition()
            distance_to_ghosts = min(manhattanDistance(successor_pos, ghost.getPosition()) for ghost in ghost_states)
            
            if distance_to_ghosts > max_distance:
                max_distance = distance_to_ghosts
                best_action = action

        return best_action

    def collectFood(self, gameState: GameState):
        def bfs(start, food_positions):
            queue = [(start, [])]
            visited = set()

            while queue:
                (x, y), path = queue.pop(0)
                if (x, y) in food_positions:
                    return path

                if (x, y) not in visited:
                    visited.add((x, y))
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # up, right, down, left
                        next_x, next_y = x + dx, y + dy
                        if not gameState.hasWall(next_x, next_y):
                            next_pos = (next_x, next_y)
                            next_path = path + [next_pos]
                            queue.append((next_pos, next_path))

            return None  # If no path to food is found

        pacman_pos = gameState.getPacmanPosition()
        food_list = gameState.getFood().asList()

        if not food_list:
            return Directions.STOP

        path_to_nearest_food = bfs(pacman_pos, set(food_list))

        if not path_to_nearest_food:
            return random.choice(gameState.getLegalActions(0))

        next_pos = path_to_nearest_food[0]
        dx, dy = next_pos[0] - pacman_pos[0], next_pos[1] - pacman_pos[1]

        if dx == 1:
            return Directions.EAST
        elif dx == -1:
            return Directions.WEST
        elif dy == 1:
            return Directions.NORTH
        elif dy == -1:
            return Directions.SOUTH
        else:
            return Directions.STOP

    def alpha_beta_search(self, gameState: GameState):
        alpha = float('-inf')
        beta = float('inf')
        best_action = None
        best_score = float('-inf')
        legal_actions = gameState.getLegalActions(0)
        action_scores = []

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            successor_pos = successor.getPacmanPosition()

            if self.avoidRevisits(successor_pos):
                continue

            score = self.alpha_beta(successor, depth=1, agentIndex=1, alpha=alpha, beta=beta)
            action_scores.append((score, action))
            
            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, best_score)

        # Add tie-breaking by random choice among equally good actions
        best_actions = [action for score, action in action_scores if score == best_score]
        if len(best_actions) > 1:
            best_action = random.choice(best_actions)

        return best_action

    def alpha_beta(self, gameState, depth, agentIndex, alpha, beta):
        if self.isTerminalState(gameState, depth):
            return self.evaluationFunction(gameState, self)

        if agentIndex == 0:  # Maximizing player (Pac-Man)
            return self.max_value(gameState, depth, alpha, beta)
        else:  # Minimizing player (Ghosts)
            return self.min_value(gameState, depth, agentIndex, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        v = float('-inf')
        legal_actions = gameState.getLegalActions(0)

        if not legal_actions:
            return self.evaluationFunction(gameState)

        for action in legal_actions:
            successor = gameState.generateSuccessor(0, action)
            successor_position = successor.getPacmanPosition()

            if self.avoidRevisits(successor_position):
                continue

            v = max(v, self.alpha_beta(successor, depth, 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        v = float('inf')
        next_agent = (agentIndex + 1) % gameState.getNumAgents()
        next_depth = depth + 1 if next_agent == 0 else depth
        legal_actions = gameState.getLegalActions(agentIndex)

        if not legal_actions:
            return self.evaluationFunction(gameState)

        for action in legal_actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            v = min(v, self.alpha_beta(successor, next_depth, next_agent, alpha, beta))
            
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v

    def isTerminalState(self, gameState, depth):
        return gameState.isWin() or gameState.isLose() or depth >= self.depth


