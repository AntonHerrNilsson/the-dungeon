from things import Wall, Gold, Door, Switch

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

def room_from_string(room_string, world, offset=(0,0)):
    room_lines = room_string.splitlines()
    x0 = offset[0]
    y0 = offset[1]
    for y, line in enumerate(reversed(room_lines)):
        for x, char in enumerate(line):
            if char == "*":
                Gold(world, (x+x0, y+y0))
            elif char == "#":
                Wall(world, (x+x0, y+y0))
                
def three_doors(world, offset=(0,0)):
    room_string = """###################
#     #     #     #
#     #     #     #
#  *  #  *  #  *  #
#     #     #     #
#     #     #     #
### ##### ##### ###
#                 #
#                 #
#                 #
#                 #
#                 #
###################"""
    room_from_string(room_string, world, offset)
    door_one = Door(world, (9,6))
    switch = Switch(world, (6,3), target=door_one.toggle)
    
