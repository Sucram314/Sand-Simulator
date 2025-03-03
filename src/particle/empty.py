from .particle import *
from .behaviour import *

class Empty(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = EMPTY,
            colour = (0,0,0),
            behaviours = []
        )