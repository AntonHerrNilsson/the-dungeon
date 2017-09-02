import bisect
import numpy
from inspect import isclass
from copy import copy

from AI.search import Problem, astar_search
from utils import UP, DOWN, LEFT, RIGHT
from world import Thing, Obstacle



class PathFindingProblem(Problem):
    
    def __init__(self, initial_state, model, goal):
        # goal can be a function with the signature goal(location, model),
        # a thing to be present (as a class) or a location
        super().__init__(initial_state)
        self.model = model
        self.goal = goal
    
    def actions(self, state):
        loc, d = state
        actions = []
        for act in [UP, RIGHT, DOWN, LEFT]:
            new_loc = tuple(numpy.array(loc)+act)
            if (new_loc in self.model.explored
                    and not self.model.things_at(new_loc, Obstacle)):
                actions.append(tuple(act))
        return actions
    
    def result(self, state, action):
        loc, d = state
        loc = tuple(numpy.array(loc) + action)
        if d != (0,0):
            d = action
        return loc, d
    
    def goal_test(self, state):
        if isclass(self.goal) and issubclass(self.goal, Thing):
            return self.model.things_at(state[0], self.goal)
        elif callable(self.goal):
            return self.goal(state[0], self.model)
        else:
            return self.goal == state[0]
    
    def step_cost(self, from_state, action, to_state):
        d = from_state[1]
        if d == (0,0) or d == action:
            return 1
        elif (-d[0], -d[1]) == action:
            return 3
        else:
            return 2
    
    def heuristic(self, state):
        try:
            goal_locs = self.goal_locs
        except AttributeError:
            goal_locs = []
            for loc in self.model.explored:
                if self.goal_test((loc, None)):
                    goal_locs.append(loc)
            self.goal_locs = goal_locs
        x1, y1 = state[0]
        # Manhattan distance to nearest goal
        if goal_locs:
            return min([abs(x2-x1) + abs(y2-y1) for x2,y2 in goal_locs])
        else:
            return 0
            
def find_path(goal, model, initial_location, initial_direction, return_direction=False):
    initial_state = (tuple(initial_location), tuple(initial_direction))
    problem = PathFindingProblem(initial_state, model, goal)
    solution = astar_search(problem)
    if solution is None:
        return None
    actions = []
    # Determine what actions a movement consists of.
    for act, d in zip(solution, [tuple(initial_direction)] + solution[:-1]):
        if act == d:
            actions.append("Forward")
        elif act == (d[1], -d[0]):
            actions.append("TurnRight")
            actions.append("Forward")
        elif act == (-d[1], d[0]):
            actions.append("TurnLeft")
            actions.append("Forward")
        elif act == (-d[0], -d[1]):
            actions.append("TurnLeft")
            actions.append("TurnLeft")
            actions.append("Forward")
    if return_direction:
        if solution:
            direction = solution[-1]
        else:
            direction = initial_direction
        return actions, direction
    else:
        return actions

def reachable_from(location, model):
    # All tiles that are reachable from the given location
    reachable = []
    edge = []
    reachable.append(tuple(location))
    edge.append(tuple(location))
    continue_loop = True
    while continue_loop:
        continue_loop = False
        for place in copy(edge):
            new_places = []
            for direction in [UP, DOWN, LEFT, RIGHT]:
                new_place = tuple(numpy.array(place)+direction)
                if not model.things_at(new_place, Obstacle) and new_place not in reachable:
                    new_places.append(new_place)
                if new_places:
                    continue_loop = True
                    reachable.extend(new_places)
                    edge.extend(new_places)
                elif place in edge:
                    edge.remove(place)
    return reachable
    



