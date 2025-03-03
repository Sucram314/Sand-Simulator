from .particle import *
from .behaviour import *
from random import uniform

class Ice(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = ICE,
            mass = 1,
            friction = 0.98,
            colour = rand_colour(180,30,90,190,40,100),
            behaviours = [Burn(chance=uniform(0.02,0.1),fuel=-1,ondeath=WATER)]
        )