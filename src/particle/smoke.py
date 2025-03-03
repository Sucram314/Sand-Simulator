from .particle import *
from .behaviour import *
from random import randint

class Smoke(Particle):
    def __init__(self,x,y):
        colour = rand_colour(0,0,60,0,0,70)
        super().__init__(
            x,y,
            state = SMOKE,
            colour = colour,
            behaviours = [Move(ya=-2,myv=0.25,passable={EMPTY,SAND,WATER,DIRT,STONE,LAVA},settle_depth=1),
                          Expire(lifetime=randint(50,100),basecolour=colour,endcolour=(0,0,0),beginfade=30,ondeath=EMPTY),
                          Scatter(rate=0.5,passable={EMPTY})]
        )