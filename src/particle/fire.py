from .particle import *
from .behaviour import *
from random import randint

def flicker():
    return (255,randint(127,255),0)

class Fire(Particle):
    def __init__(self,x,y):
        super().__init__(
            x,y,
            state = FIRE,
            colour = flicker(),
            behaviours = [Expire(lifetime=randint(20,50),beginfade=10,flickercolour=flicker,endcolour=rand_colour(0,0,60,0,0,70),ondeath=SMOKE)]
        )