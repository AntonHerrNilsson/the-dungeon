import numpy
import random

from things import Thing, Obstacle, Wall, Gold


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
    
def testing_room(world, x_size=10, y_size=10):
    # Just a small room to test pathfinding.
    for x in range(x_size):
        Wall(world, location=(x, 0))
        Wall(world, location=(x, y_size - 1))
    for y in range(y_size):
        Wall(world, location=(0, y))
        Wall(world, location=(x_size -1, y))
    for to_spawn, amount in [(Wall, 10), (Gold, 10)]:
        for i in range(amount):
            cont = True
            while cont:
                x = random.randrange(0, x_size)
                y = random.randrange(0, y_size)
                cont = world.things_at((x,y))
            to_spawn(world, location=(x,y))


