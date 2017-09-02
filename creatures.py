import numpy
import IPython

from things import Thing, Obstacle, Gold
from utils import IDENTITY, rotate_back_matrix, UP, DOWN, LEFT, RIGHT
import symbols


class Player(Thing):
    """The main character"""
    
    def __init__(self, world, location, ai_class=None, direction=(0,1), **kwargs):
        super().__init__(world, location, direction, **kwargs)
        if not ai_class is None:
            self.ai = ai_class()
        self.score = 0
    
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
        for y in range(-20,21):
            for x in range(-20,21):
                loc = (x,y)
                true_loc = self.location + m.dot(loc)
                if self.world.outside_world(true_loc):
                    continue
                percieved[loc] = []
                for thing in self.world.things_at(true_loc):
                    if thing.symbol() is not None:
                        percieved[loc].append((thing.symbol(), thing.color))
        return percieved
    
    def do_action(self, action):
        if action.startswith("Get"): # e.g. "Get *"
            char_with_color = action.split()[1]
            char = symbols.strip_color(char_with_color)
            color = symbols.get_color(char_with_color)
            things = [thing for thing in self.world.things_at(self.location) if thing.symbol() == char and thing.color == color]
            if things:
                thing = things[0]
                try:
                    thing.get(actor=self)
                except AttributeError:
                    print("Tried to get something that is not gettable.")
        elif action.startswith("Activate"):
            char_with_color = action.split()[1]
            char = symbols.strip_color(char_with_color)
            color = symbols.get_color(char_with_color)
            things = [thing for thing in self.world.things_at(self.location) if thing.symbol() == char and thing.color == color]
            if things:
                thing = things[0]
                try:
                    thing.activate(actor=self)
                except AttributeError:
                    print("Tried to activate something that is not activatable.")
                
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
            self.score -= 1
        
    def symbol(self):
        d = tuple(self.direction)
        if d == tuple(RIGHT):
            return symbols.PLAYER_RIGHT
        elif d == tuple(UP):
            return symbols.PLAYER_UP
        elif d == tuple(LEFT):
            return symbols.PLAYER_LEFT
        elif d == tuple(DOWN):
            return symbols.PLAYER_DOWN
    
