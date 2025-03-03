from .particle import *
from .behaviour import *
from random import randint

class Lava(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = LAVA,
            mass = 1,
            friction = 0.9,
            colour = (255,randint(0,127),0),
            behaviours = [Move(ya=1,settle_depth=0,disperse=0.5,max_boost=5,div_y=2,passable={EMPTY,SMOKE}),
                          Obliterate(reactions={WATER:(1,STONE,SMOKE)})]
        )