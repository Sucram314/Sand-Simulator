from .particle import *
from .behaviour import *

class Stone(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = STONE,
            colour = rand_colour(0,0,30,0,0,40),
            mass = 2,
            friction = 0.7,
            behaviours = [Move(ya=1,passable={EMPTY,WATER,SMOKE,LAVA},replacable={FIRE,SNOW},settle_depth=-1)]
        )