import numpy

# Transform matrices
IDENTITY = numpy.array(((1,0),
                        (0,1)))

ROTATE_LEFT = numpy.array(((0,-1),
                           (1, 0)))
                           
ROTATE_RIGHT = numpy.array((( 0,1),
                            (-1,0)))
                            
def rotate_back_matrix(forward_direction):
    x = forward_direction[0]
    y = forward_direction[1]
    return numpy.array((( y,x),
                         (-x,y)))
    

# Directions
UP = numpy.array((0,1))
DOWN = numpy.array((0,-1))
LEFT = numpy.array((-1,0))
RIGHT = numpy.array((1,0))
