from .behaviour import *
from random import random

"""
reactions should be a ditionary of ELEMENT:(chance,ondeath_self,ondeath_other)

e.g. water reaction={FIRE:(EMPTY,SMOKE)}
"""

class Obliterate(Behaviour):
    def __init__(self,reactions={}):
        super().__init__(B_OBLITERATE)
        self.reactions = reactions
        
    def update(self,x,y,scene):
        flag = 0

        for dx,dy in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            if not scene.within(x+dx,y+dy): continue

            state = scene.grid[y+dy][x+dx].state
            if state in self.reactions:
                chance,statea,stateb = self.reactions[state]

                if random() <= chance:
                    flag = 2
                    scene.set_at(x,y,statea)
                    scene.set_at(x+dx,y+dy,stateb)

        return flag