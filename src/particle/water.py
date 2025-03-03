from .particle import *
from .behaviour import *
from random import uniform

class Water(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = WATER,
            mass = 1,
            friction = 0.9,
            colour = rand_colour(190,80,80,200,100,100),
            behaviours = [Move(ya=1,settle_depth=0,disperse=5,max_boost=5,div_y=2,passable={EMPTY,SMOKE}),
                          Obliterate(reactions={FIRE:(1,EMPTY,SMOKE),ICE:(uniform(0.2,0.5)**3,ICE,ICE)})]
        )