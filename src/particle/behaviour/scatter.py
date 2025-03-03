from .behaviour import *
from random import random,randint

class Scatter(Behaviour):
    def __init__(self,rate=1,passable={EMPTY}):
        super().__init__(B_SCATTER)
        self.rate = rate
        self.passable = passable
        
    def update(self,x,y,scene):
        if random() > self.rate: return 0

        left = x > 0 and scene.grid[y][x-1].state in self.passable
        right = x < scene.w - 1 and scene.grid[y][x+1].state in self.passable

        if left:
            if right:
                scene.swap(x,y,x+randint(0,1)*2-1,y)
            else:
                scene.swap(x,y,x-1,y)
        else:
            if right:
                scene.swap(x,y,x+1,y)
            else:
                return 0
            
        return 1