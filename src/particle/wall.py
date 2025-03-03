from .particle import *
from .behaviour import *

class Wall(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = WALL,
            mass = 999,
            friction = 0.8,
            colour = (0,15,43) if y % 4 == 0 or x % 10 == y // 4 % 2 * 5 else (0,30,87),
            behaviours = []
        )