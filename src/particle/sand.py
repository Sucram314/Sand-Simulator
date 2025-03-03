from .particle import *
from .behaviour import *

class Sand(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = SAND,
            mass = 1,
            friction = 0.8,
            colour = rand_colour(40,50,80,50,80,100),
            behaviours = [Move(ya=1,passable={EMPTY,WATER,SMOKE,LAVA},replacable={FIRE},settle_depth=1,disperse=1.5,max_boost=5,div_y=2)]
        )