import numpy

from world import World
from things import Thing, Gold, Wall, Door, Switch
from utils import IDENTITY, rotate_back_matrix
import utils
import symbols

class Model(World):
    # Functionality has been added to track whether a tile has been 
    # explored or not. 
    
    def __init__(self):
        super().__init__()
        self.explored = []
        self.owner = None
    
    def things_at(self, location, thing_class=Thing):
        if tuple(location) in self.explored:
            return super().things_at(location, thing_class)
        else:
            return [Unexplored()]
    
    

class Unexplored(object):
    # An object representing the fact that a tile has not been explored.
    def __init__(self):
        self.color = None
    
    def symbol(self):
        return symbols.UNEXPLORED
