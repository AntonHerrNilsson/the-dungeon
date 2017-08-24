import numpy

from world import World
from things import Thing, Gold, Wall
from utils import IDENTITY, rotate_back_matrix

class Model(World):
    # Functionality has been added to track whether a tile has been 
    # explored or not, and explore tiles.
    
    def __init__(self):
        super().__init__()
        self.explored = []
    
    def as_expected(self, location, symbols):
        for thing, symbol in zip(self.things_at(location), symbols):
            if thing.symbol() != symbol:
                return False
        return True
    
    def update(self, percept, loc, d):
        # The percept is probably shifted and rotated with respect to
        # the model.
        if tuple(d) == (0,0):
            m = IDENTITY
        else:
            m = rotate_back_matrix(d)
        for place in percept:
            true_place = tuple(loc + m.dot(place))
            if true_place in self.explored:
                if self.as_expected(true_place, percept[place]):
                    continue
                else: # Just replace everything if something is wrong.
                    print("Something unexpected here!")
                    for thing in self.things_at(true_place):
                        self.remove_thing(thing)
            else:
                self.explored.append(true_place)
            # Remember, this will only happen if the place is unexplored
            # or things were not as expected.
            for symbol in percept[place]:
                if symbol == "*":
                    Gold(self, true_place)
                elif symbol == "#":
                    Wall(self, true_place)
    
    def things_at(self, location, thing_class=Thing):
        if tuple(location) in self.explored:
            return super().things_at(location, thing_class)
        else:
            return [Unexplored()]

class Unexplored(object):
    # An object representing the fact that a tile has not been explored.
    
    def symbol(self):
        return "\u2591"
