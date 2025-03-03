from .particle import *
from .behaviour import *
from random import uniform

class Snow(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = SNOW,
            mass = 0.2,
            friction = 0.92,
            colour = rand_colour(0,0,90,0,0,100),
            behaviours = [Move(ya=2,myv=1,passable={EMPTY,SMOKE},settle_depth=1),
                          Scatter(rate=0.5,passable={EMPTY,SMOKE}),
                          Obliterate(reactions={WATER:(uniform(0.2,0.5)**3,WATER,WATER),ICE:(1,ICE,ICE),LAVA:(1,SMOKE,LAVA)}),
                          Burn(chance=0.5,fuel=-1,ondeath=WATER)]
        )