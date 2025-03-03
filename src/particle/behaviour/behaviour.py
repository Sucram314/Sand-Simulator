from abc import ABC
from colorsys import hsv_to_rgb
from random import randint
from ..consts import *
from .consts import *

class Behaviour(ABC):
    def __init__(self,name):
        self.name = name

    def update(self,x,y,scene):
        return True
    
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