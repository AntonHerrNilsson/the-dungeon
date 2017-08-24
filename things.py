import numpy

from utils import ROTATE_LEFT, ROTATE_RIGHT


class Thing:
    """Something that can exist in the world."""
    
    def __init__(self, world, location, direction=(0,0)):
        self.direction = direction
        self.world = world
        self.world.add_thing(self, location)
    
    @property
    def location(self):
        return self.world.things[self]
    
    @location.setter
    def location(self, value):
        self.world.move_thing(self, value)
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = numpy.array(value)
        
    def move(self, relative_location):
        self.location = self.location + relative_location
            
    def turn_left(self):
        self.direction = ROTATE_LEFT.dot(self.direction)
    
    def turn_right(self):
        self.direction = ROTATE_RIGHT.dot(self.direction)
    
    def move_forward(self):
        self.move(self.direction)
    
    def symbol(self):
        raise NotImplementedError

class Obstacle(Thing):
    """Something that prevents movement into its location."""
    pass
    
class Wall(Obstacle):
    """Just an ordinary wall."""
    
    def symbol(self):
        return "#"

class Gold(Thing):
    """When you pick it up you become happy"""
    
    def symbol(self):
        return "*"
        
            
