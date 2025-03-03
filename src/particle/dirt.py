from .particle import *
from .behaviour import *

class Dirt(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = DIRT,
            mass = 1,
            friction = 0.85,
            colour = rand_colour(25,80,30,35,100,40),
            behaviours = [Move(ya=1,passable={EMPTY,WATER,SMOKE,LAVA},replacable={FIRE},settle_depth=2,disperse=1.5,max_boost=5,div_y=2)]
        )