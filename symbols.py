import pyparsing
import IPython

# Symbols

PLAYER_UP    = "^"
PLAYER_RIGHT = ">"
PLAYER_DOWN  = "v"
PLAYER_LEFT  = "<" 

WALL = "#"
GOLD = "*"

OPEN_DOOR = "\u16A2"
CLOSED_DOOR = "\u16A5"
SWITCH = "!"

UNEXPLORED = "\u2591"

# Symbol colors

LIGHT_BLUE = "\033[94m"
BLUE = "\x1b[34m"
GREEN = "\x1b[32m"

# Manipulating colors

def apply_color(char, color):
    if char is not None:
        if color is not None:
            return color + char + "\033[0m"
        else:
            return char
    else:
        return None

def same(first, second):
    # Check if two symbols are the same, not taking color into account
    return strip_color(first) == strip_color(second)

def strip_color(string):
    if string is not None:
        # Stripping out color codes
        # https://stackoverflow.com/questions/2186919/getting-correct-string-length-in-python-for-strings-with-ansi-color-codes
        ESC = pyparsing.Literal('\x1b')
        integer = pyparsing.Word(pyparsing.nums)
        escapeSeq = pyparsing.Combine(ESC + '[' + pyparsing.Optional(pyparsing.delimitedList(integer,';')) + 
                        pyparsing.oneOf(list(pyparsing.alphas)))
        nonAnsiString = lambda s : pyparsing.Suppress(escapeSeq).transformString(s)
        unColorString = nonAnsiString(string)
        return unColorString
    else:
        return None

def get_color(symbol):
    # get the color of a single symbol. I don't really understand how this works.
    ESC = pyparsing.Literal('\x1b')
    integer = pyparsing.Word(pyparsing.nums)
    escapeSeq = pyparsing.Combine(ESC + '[' + pyparsing.Optional(pyparsing.delimitedList(integer,';')) + 
                    pyparsing.oneOf(list(pyparsing.alphas)))
    item =  next(escapeSeq.scanString(symbol), None)
    if item is not None:
        return item[0][0]
    else:
        return None
        
