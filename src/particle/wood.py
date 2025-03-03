from .particle import *
from .behaviour import *
from random import uniform,randint

class Wood(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = WOOD,
            mass = 999,
            friction = 0.7,
            colour = rand_colour(20,80,15,30,100,25),
            behaviours = [Burn(uniform(0.02,0.2),fuel=randint(50,150))]
        )