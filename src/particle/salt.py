from .particle import *
from .behaviour import *
from random import uniform

class Salt(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = SALT,
            mass = 1,
            friction = 0.8,
            colour = rand_colour(0,0,70,0,0,90),
            behaviours = [Move(ya=1,passable={EMPTY,WATER,SMOKE,LAVA},replacable={FIRE},settle_depth=1,disperse=1.5,max_boost=5,div_y=2),
                          Obliterate({ICE:(uniform(0.1,0.5),SALT,WATER)})]
        )