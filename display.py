import pyparsing

from world import World


def display(tick, score, centers, radius, *args):
    args = list(args)
    display_str = None
    for arg, center in zip(args, centers):
        if isinstance(arg, World):
            arg_str = world_string(arg, radius, center)
        elif isinstance(arg, dict):
            arg_str = percept_string(arg)
        if display_str is None:
            display_str = prettify(arg_str)
        else:
            display_str = combine_displays(display_str, prettify(arg_str))
    print("\033[1;1H")
    print(display_str)
    for i, ticktype in enumerate(["-","/","|","\\"]):
        if tick % 4 == i:
            print(ticktype + " " + str(score))
            
def initialize():
    for i in range(50):
        print("")

def combine_displays(left, right, spaces_between=10):
    left_lines = left.splitlines()
    right_lines = right.splitlines()
    # Make sure the right and left parts have the same amount of lines.
    extra_lines = len(left_lines) - len(right_lines)
    if not extra_lines == 0:
        if extra_lines < 0:
            shorter = left_lines
            extra_lines *= -1
        else:
            shorter = right_lines
        above = extra_lines // 2
        below = extra_lines - above
        empty_line = len(shorter[0])*" "
        shorter[0:0] = [empty_line]*above
        shorter.extend([empty_line]*below)
    display = ""
    for i,line in enumerate(left_lines):
        display += line
        display += " " * spaces_between
        display += right_lines[i]
        display += "\n"
    return display

def world_string(world, radius, center=None):
    # Do not be fooled by the radius, this returns a square map. 
    # If center is None, the entire world is shown instead.
    if center is None:
        x_start = min([loc[0] for loc in world.locations])
        y_start = min([loc[1] for loc in world.locations])
        x_end = max([loc[0] for loc in world.locations]) + 1
        y_end = max([loc[1] for loc in world.locations]) + 1
    else:
        x_start = center[0] - radius
        x_end = center[0] + radius + 1
        y_start = center[1] - radius
        y_end = center[1] + radius + 1
    world_string = ""
    for y in reversed(range(y_start, y_end)):
        for x in range(x_start, x_end):
            things = world.things_at((x,y))
            if things:
                thing = things[0]
                world_string += thing.symbol()
            else:
                world_string += " "
            
        world_string += "\n"
    return world_string
    
def percept_string(percept):
    x_start = min([key[0] for key in percept])
    y_start = min([key[1] for key in percept])
    x_end = max([key[0] for key in percept]) + 1
    y_end = max([key[1] for key in percept]) + 1
    out_string = ""
    for y in reversed(range(y_start, y_end)):
        for x in range(x_start, x_end):
            things = percept[(x,y)]
            if things:
                thing = things[0]
                if thing in [">", "v", "<"]:
                    thing = "^"
                out_string += thing
            else:
                out_string += " "
        out_string += "\n"
    return out_string
    
def prettify(string):
    lines = string.splitlines()
    # Stripping out color codes
    # https://stackoverflow.com/questions/2186919/getting-correct-string-length-in-python-for-strings-with-ansi-color-codes
    ESC = pyparsing.Literal('\x1b')
    integer = pyparsing.Word(pyparsing.nums)
    escapeSeq = pyparsing.Combine(ESC + '[' + pyparsing.Optional(pyparsing.delimitedList(integer,';')) + 
                    pyparsing.oneOf(list(pyparsing.alphas)))
    nonAnsiString = lambda s : pyparsing.Suppress(escapeSeq).transformString(s)
    unColorString = nonAnsiString(lines[0])
    width = len(unColorString)
    #IPython.embed()
    new_string = "╔" + width*"═" + "╗\n"
    for line in lines:
        new_string += "║" + line + "║\n"
    new_string += "╚" + width*"═" + "╝\n"
    return new_string
