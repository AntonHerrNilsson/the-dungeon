import random
from copy import copy, deepcopy
import IPython

from AI import pathfinding
from AI.door_handling import AbstractedDoorProblem
import search
from creatures import Player
from things import Gold
import model
import symbols
import utils
from things import Wall, Gold, Door, Switch
import display

class PlayerAI:
    
    def __init__(self):
        self.model = model.Model()
        self.self_model = Player(world=self.model, location=(0,0))
        self.model.owner = self.self_model
        self.plan = []
        
    def __call__(self, percept):
        return self.program(percept)
    
    def update_model(self, percept):
        self.model.step()
        loc = self.self_model.location
        d = self.self_model.direction
        # The percept is probably shifted and rotated with respect to
        # the model.
        if tuple(d) == (0,0): # Just in case I do not have a direction
            m = utils.IDENTITY
        else:
            m = utils.rotate_back_matrix(d)
        for place in percept:
            true_place = tuple(loc + m.dot(place))
            if true_place not in self.model.explored:
                self.model.explored.append(true_place)
                self.fill_place(percept[place], true_place)
                self.modify_plan(percept[place], true_place)
            elif not self.as_expected(percept[place], true_place):
                self.handle_mismatch(percept[place], true_place)
        
    def handle_mismatch(self, percept_part, location):
        # Just replace everything if something is wrong.
        print("Something unexpected here!")
        for thing in self.model.things_at(location):
            self.model.remove_thing(thing)
        self.fill_place(percept[place], true_place)
        self.modify_plan(percept_part, location)
    
    def fill_place(self, percept_part, location):
        # Fill in a place with objects according to the percept.
        # Assumes none of the objects are in the model already, or they will be duplicated.
        for p in percept_part:
            symbol = p[0]
            color = p[1]
            if symbol == symbols.GOLD:
                thing = Gold(self.model, location, color=color)
            elif symbol == symbols.WALL:
                thing = Wall(self.model, location, color=color)
            elif symbol == symbols.CLOSED_DOOR:
                thing = Door(self.model, location, closed=True, color=color)
            elif symbol == symbols.OPEN_DOOR:
                thing = Door(self.model, location, closed=False, color=color)
            elif symbol == symbols.SWITCH:
                thing = Switch(self.model, location, color=color)
            else:
                thing = None
            # Assume that switches always toggle the door of the same color, for now.
            if isinstance(thing, Door):
                switches = [thing for thing in self.model.things
                            if isinstance(thing, Switch) 
                                and thing.color == color]
                for switch in switches:
                    switch.add_target(thing.toggle)
            if isinstance(thing, Switch):
                doors = [thing for thing in self.model.things
                            if isinstance(thing, Door) 
                                and thing.color == color]
                for door in doors:
                    thing.add_target(door.toggle)
                
                
    
    def modify_plan(self, percept_part, location):
        # If new information comes to light, modify the plan. 
        # In this case, just scrap it.
        self.plan = []
    
    def as_expected(self, percept_part, location):
        for thing, p in zip([thing for thing in self.model.things_at(location) if thing.symbol() is not None], percept_part):
            symbol = p[0]
            color = p[1]
            if not (thing.symbol() == symbol and thing.color == color):
                return False
        return True
    
    def make_plan(self):
        loc = self.self_model.location
        d = self.self_model.direction
        plan = pathfinding.find_path(Gold, self.model, loc, d)
        if plan is None:
            plan = ["NoOp"]
        else:
            plan += ["Get " + symbols.GOLD] # This will break if the gold has a color, be advised.
        self.plan = plan
            
    
    def program(self, percept):
        self.update_model(percept)
        if not self.plan:
            self.make_plan()
        action = self.plan.pop(0)
        self.self_model.do_action(action)
        return action
        
class DoorCompetentAI(PlayerAI):
    
    def make_plan(self):
        problem = AbstractedDoorProblem(self.model)
        high_level_actions = search.astar_search(problem)
        actions = problem.expand_solution(high_level_actions)
        if actions:
            self.plan = actions
        else:
            self.plan = ["NoOp"]
        
        
    

        
        

            
