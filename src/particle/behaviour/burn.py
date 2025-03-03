from .behaviour import *
from random import random

class Burn(Behaviour):
    def __init__(self,chance=1,fuel=50,ondeath=FIRE):
        super().__init__(B_BURN)
        self.chance = chance
        self.fuel = fuel
        self.ondeath = ondeath
        
    def update(self,x,y,scene):
        for dx,dy in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
            if not scene.within(x+dx,y+dy): continue

            state = scene.grid[y+dy][x+dx].state

            if state == FIRE and random() <= self.chance:
                scene.set_at(x,y,self.ondeath)
                if self.fuel != -1: scene.grid[y][x].get_behaviour(B_EXPIRE).lifetime = self.fuel
                return 2
            
            if state == LAVA and random() >= (1 - self.chance) ** 3:
                scene.set_at(x,y,self.ondeath)
                if self.fuel != -1: scene.grid[y][x].get_behaviour(B_EXPIRE).lifetime = self.fuel
                return 2

        return 0