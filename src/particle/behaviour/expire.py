from .behaviour import *

class Expire(Behaviour):
    def __init__(self,lifetime=100,basecolour=(255,255,255),flickercolour=None,endcolour=(0,0,0),beginfade=50,ondeath=EMPTY):
        super().__init__(B_EXPIRE)
        self.lifetime = lifetime
        self.basecolour = basecolour
        self.flickercolour = flickercolour
        self.endcolour = endcolour
        self.beginfade = beginfade
        self.ondeath = ondeath
        
    def update(self,x,y,scene):
        self.lifetime -= 1

        if self.flickercolour:
            self.basecolour = self.flickercolour()
            if self.lifetime >= self.beginfade:
                scene.grid[y][x].colour = self.basecolour

        if self.lifetime < self.beginfade:
            t = self.lifetime / self.beginfade
            scene.grid[y][x].colour = (self.basecolour[0] * t, self.basecolour[1] * t, self.basecolour[2] * t)

        scene.flag(x,y)

        if self.lifetime == 0:
            scene.set_at(x,y,self.ondeath)
            return 2

        return 1