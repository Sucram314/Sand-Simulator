from abc import ABC
from colorsys import hsv_to_rgb
from random import randint
from .behaviour import *
from .consts import *

class Particle(ABC):
    def __init__(self,x,y,state,colour,mass=1,friction=0.8,behaviours=[]):
        self.x = x
        self.y = y
        self.state = state
        self.colour = colour
        self.mass = mass
        self.friction = friction
        self.update_direction = 1
        self.behaviours = behaviours
        self.lookup = {b.name:b for b in self.behaviours}

    def update(self,scene,direction):
        if direction != self.update_direction: return False

        res = False
        for b in self.behaviours:
            result = b.update(self.x,self.y,scene)
            res = result | res
            if result == 2: #identity change
                break

        return res

    def get_behaviour(self,name):
        return self.lookup[name] if name in self.lookup else None

def conv(h,s,v):
    h /= 360
    s /= 100
    v /= 100

    r,g,b = hsv_to_rgb(h,s,v)

    r = round(r*255)
    g = round(g*255)
    b = round(b*255)

    return r,g,b

def rand_colour(h1,s1,v1,h2,s2,v2):
    return conv(randint(h1,h2), randint(s1,s2), randint(v1,v2))