import numpy

from things import Thing, Obstacle, Gold
from utils import IDENTITY, rotate_back_matrix, UP, DOWN, LEFT, RIGHT


class Player(Thing):
    """The main character"""
    
    def __init__(self, world, location, ai_class=None, direction=(0,1)):
        super().__init__(world, location, direction)
        if not ai_class is None:
            self.ai = ai_class()
        self.performance = 0
    
    def percept(self):
        percieved = {}
        # We need to transform the coordinates, as the player should see its own direction as "up"
        if tuple(self.direction) == (0,0):
            # If the agent doesn't have a direction, just keep the world
            # directions as they are
            m = IDENTITY
        else:
            # Else, the agent should see the way it is facing as "up".
            m = rotate_back_matrix(self.direction)
        # Just percieve everything in a hardcoded square for now
        for y in range(-10,11):
            for x in range(-10,11):
                loc = (x,y)
                percieved[loc] = []
                for thing in self.world.things_at(self.location + m.dot(loc)):
                    percieved[loc].append(thing.symbol())
        return percieved
    
    def do_action(self, action):
        if action.startswith("Get"): # e.g. "Get *"
            char = action.split()[1]
            things = [thing for thing in self.world.things_at(self.location) if thing.symbol() == char]
            if things:
                thing = things[0]
                if isinstance(thing, Gold): # Only gold is implemented right now.
                    self.performance += 100
                    self.world.remove_thing(thing)
        elif action == "TurnRight":
            self.turn_right()
        elif action == "TurnLeft":
            self.turn_left()
        elif action == "Forward":
            self.move_forward()
        elif action == "ShutDown":
            if hasattr(self, "ai"):
                del self.ai
        elif action == "NoOp":
            pass
        if action != "NoOp":
            self.performance -= 1
        
    def symbol(self):
        d = tuple(self.direction)
        if d == tuple(RIGHT):
            return ">"
        elif d == tuple(UP):
            return "^"
        elif d == tuple(LEFT):
            return "<"
        elif d == tuple(DOWN):
            return "v"
    
