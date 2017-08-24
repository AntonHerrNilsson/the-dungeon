import random

import pathfinding
from creatures import Player
from things import Gold
import model

class PlayerAI:
    
    def __init__(self):
        self.model = model.Model()
        self.self_model = Player(world=self.model, location=(0,0))
        self.plan = []
        
    def __call__(self, percept):
        return self.program(percept)
    
    def update_model(self, percept):
        self.model.step()
        loc = self.self_model.location
        d = self.self_model.direction
        self.model.update(percept, loc, d)
    
    def decide_action(self):
        if not self.plan:
            loc = self.self_model.location
            d = self.self_model.direction
            plan = pathfinding.find_path(Gold, self.model, loc, d)
            if plan is None:
                plan = ["NoOp"]
            else:
                plan += ["Get *"]
            self.plan = plan
        return self.plan.pop(0)
            
    
    def program(self, percept):
        self.update_model(percept)
        action = self.decide_action()
        self.self_model.do_action(action)
        return action
        
        

            
