import numpy
import random
import pickle
import IPython

from things import Thing, Obstacle, Wall, Gold
from display import world_string


class World:
    """The environment in which everything takes place."""

    def __init__(self):
        # We want to be able to quickly get the location of a thing,
        # and things at a location. So we have two dicts.
        # The first has object ID as key and location as value
        self.things = {}
        # The second has location (as a tuple) as key and a list of
        # objects as value. Things earlier in the list are on top of
        # later ones.
        self.locations = {}
    
    def step(self):
        # First, every agent should do what it does. 
        # Currently, order of priority is not important.
        for agent in [thing for thing in 
                        self.things if hasattr(thing, "ai")]:
            perception = agent.percept()
            action = agent.ai(perception)
            agent.do_action(action)
        # Non-agent things might do stuff here later.
    
    def add_thing(self, thing, location):
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            self.things[thing] = numpy.array(location)
            if not tuple(location) in self.locations:
                self.locations[tuple(location)] = []
            self.locations[tuple(location)].insert(0, thing)
            
    def remove_thing(self, thing):
        if thing not in self.things:
            print("Can't remove what doesn't exist")
        else:
            loc = tuple(self.things[thing])
            del self.things[thing]
            self.locations[loc].remove(thing)
            # Remove the list if it is empty
            if not self.locations[loc]:
                del self.locations[loc]
    
    def move_thing(self, thing, loc):
        # Move something, but not if there is an obstacle there.
        if not self.things_at(loc, Obstacle):
            old_loc = tuple(self.things[thing])
            self.things[thing] = numpy.array(loc)
            self.locations[old_loc].remove(thing)
            if not self.locations[old_loc]:
                del self.locations[old_loc]
            if tuple(loc) not in self.locations:
                self.locations[tuple(loc)] = []
            self.locations[tuple(loc)].insert(0, thing)
    
    def things_at(self, location, thing_class=Thing):
        # Return everything at a location, 
        # or only things of type thing_class.
        loc = tuple(location)
        things = [thing for thing in self.locations.get(loc, []) 
                                if isinstance(thing, thing_class)]
        return things
    
    def outside_world(self, location):
        # Checks if the location is outside the defined world, so that it is not perceptible.
        x, y = tuple(location)
        return (x < min([key[0] for key in self.locations])
                 or y < min([key[1] for key in self.locations])
                 or x > max([key[0] for key in self.locations])
                 or y > max([key[1] for key in self.locations]))
    
        
            




