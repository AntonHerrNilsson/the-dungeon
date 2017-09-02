

import search
from copy import deepcopy
from things import Switch, Gold, Door
from AI import pathfinding
import symbols

class AbstractedDoorProblem(search.Problem):
    
    def __init__(self, model):
        self.model = deepcopy(model)
        self.switches = tuple([thing for thing in self.model.things
                        if isinstance(thing, Switch)])
        self.gold = tuple([thing for thing in self.model.things
                        if isinstance(thing, Gold)])
        self.doors = tuple([thing for thing in self.model.things
                        if isinstance(thing, Door)])
        gold_taken = (False,) * len(self.gold)
        doors_closed = tuple([door.closed for door in self.doors])
        location = tuple(self.model.owner.location)
        direction = tuple(self.model.owner.direction)
        initial_state = (gold_taken, doors_closed, location, direction)
        super().__init__(initial_state)
        self.paths_and_directions = {}
    
    def actions(self, state):
        actions = []
        self.make_model_match_state(state)
        gold_taken, doors_closed, location, direction = state
        reachable = pathfinding.reachable_from(location, self.model)
        for gold, taken in zip(self.gold, gold_taken):
            if (not taken) and (tuple(gold.location) in reachable):
                actions.append(gold)
        for switch in self.switches:
            if tuple(switch.location) in reachable:
                actions.append(switch)
        return actions
    
    def result(self, state, action):
        thing = action
        gold_taken, doors_closed, location, direction = state
        if thing in self.gold:
            gold_taken = tuple([taken or gold == action for gold, taken in zip(self.gold, gold_taken)])
        if thing in self.switches:
            self.make_model_match_state(state)
            thing.activate(self.model.owner)
            doors_closed = self.get_closed_doors()
        location = tuple(thing.location)
        direction = self.get_path_and_direction(state, action)[1]
        new_state = (gold_taken, doors_closed, location, direction)
        return new_state
    
    def get_path_and_direction(self, state, action):
        gold_taken, doors_closed, location, direction = state
        goal = tuple(action.location)
        # We throw away gold_taken, since it doesn't matter for the path
        key = (doors_closed, location, direction, goal)
        if key not in self.paths_and_directions:
            self.make_model_match_state(state)
            actions, direction = pathfinding.find_path(goal, self.model, 
                                    location, direction, return_direction=True)
            path = actions
            self.paths_and_directions[key] = (path, direction)
        return self.paths_and_directions[key]   
    
    def goal_test(self, state):
        gold_taken, doors_closed, location, direction = state
        return all(gold_taken)
    
    def step_cost(self, from_state, action, to_state):
        # Add one because you need to do something when you're there.
        return len(self.get_path_and_direction(from_state, action)[0]) + 1
    
    def heuristic(self, state):
        return 0
            
    def make_model_match_state(self, state):
        gold_taken, doors_closed, location, direction = state
        for door, closed in zip(self.doors, doors_closed):
            if closed:
                door.close()
            else:
                door.open()
    
    def get_closed_doors(self):
        return tuple([door.closed for door in self.doors])
    
    def expand_solution(self, high_level_actions):
        if high_level_actions is None:
            return None
        actions = []
        state = self.initial_state
        for action in high_level_actions:
            path = self.get_path_and_direction(state, action)[0]
            actions += path
            thing = action
            symbol = symbols.apply_color(thing.symbol(), thing.color)
            if isinstance(thing, Gold):
                actions += ["Get "+symbol]
            elif isinstance(thing, Switch):
                actions += ["Activate "+symbol]
            state = self.result(state, action)
        return actions
