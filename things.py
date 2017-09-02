import numpy
import IPython

import symbols
import utils
from utils import ROTATE_LEFT, ROTATE_RIGHT


class Thing:
    """Something that can exist in the world."""
    
    def __init__(self, world, location, direction=(0,0), color=None):
        self.direction = direction
        self.world = world
        self.world.add_thing(self, location)
        self.color = color
    
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
        # Return a character, or several if escape sequences are used. Return None if the thing is invisible.
        raise NotImplementedError


class Obstacle(Thing):
    """Something that prevents movement into its location."""
    pass
    
class Wall(Obstacle):
    """Just an ordinary wall."""
    
    def symbol(self):
        return symbols.WALL

class Gold(Thing):
    """When you pick it up you become happy"""
    
    def get(self, actor):
        self.world.remove_thing(self)
        actor.score += 100
    
    def symbol(self):
        return symbols.GOLD

class Door(Thing):
    
    def __init__(self, world, location, closed=True, **kwargs):
        super().__init__(world, location, **kwargs)
        self.blocker = None
        if closed:
            self.close()
        else:
            self.open()
    
    def close(self):
        self.closed = True
        if self.blocker is None:
            self.blocker = InvisibleWall(self.world, self.location)
    
    def open(self):
        self.closed = False
        if self.blocker is not None:
            self.world.remove_thing(self.blocker)
            self.blocker = None
    
    def toggle(self):
        if self.closed:
            self.open()
        else:
            self.close()
    
    def symbol(self):
        if self.closed:
            return symbols.CLOSED_DOOR
        else:
            return symbols.OPEN_DOOR

class InvisibleWall(Obstacle):
    
    def symbol(self):
        return None

class Switch(Thing):
    
    def __init__(self, world, location, target=None, **kwargs):
        # target should be a method, like door.toggle
        super().__init__(world, location, **kwargs)
        if target is None:
            self.targets = []
        else:
            self.targets= [target]
    
    def add_target(self, target):
        if target not in self.targets:
            self.targets.append(target)
    
    def remove_target(self, target):
        if target in self.targets:
            self.targets.remove(target)
    
    def activate(self, actor):
        for target in self.targets:
            target()
    
    def symbol(self):
        return symbols.SWITCH
            

        
    
            
